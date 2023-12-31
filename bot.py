#絵文字を自動生成するdiscord bot

import discord
from PIL import Image, ImageDraw, ImageFont
import json
from os import path
import random
import math
import csv
import requests
#import MeCab
from goolabs import GoolabsAPI

#あとから変更するかもしれない変数
size = 128 #画像のサイズ
help_message = """
### 通常の使い方
`;｛テキスト｝;`という形式でメッセージを送信すると、そのメッセージを絵文字に変換して送信します。
:oharagi:や:oyasuragi:のような絵文字に変換されます。
入力された文字はローマ字としてひらがなに変換され、必要に応じて漢字に変換されます。
### 絵文字を削除する
このbotで送信した絵文字は送信者に偽造したwebhookで送信されているため、管理者権限を持っていないと本来の方法での削除はできません。
絵文字を削除したい場合は、削除したい絵文字に`D`または`de`と送信してください。
### コマンド一覧
`/emoji ｛テキスト｝`: 任意の文字列を絵文字として送信できます。
`/help`: このヘルプを表示します。
"""


#定数の設定
this_dir = __file__[:-6] #このファイルのディレクトリ
temp_file = this_dir + "temp\emoji.png"
intents = discord.Intents.all() #botにすべての権限を与える
bot = discord.Bot(intents=intents, command_prefix="/")
romaji_to_japanese_map = {} #ローマ字ひらがな変換マップの定義

#config.jsonから設定を読み込む
with open(path.join(path.dirname(__file__), "config.json"), "r") as f:
    config = json.load(f)
token = config["token"]
app_id = config["app_id"]

#形態素解析APIの設定
gooAPI = GoolabsAPI(app_id)

#フォントのパスを取得
font_path = path.join(path.dirname(__file__), "NotoSansJP-Bold.ttf")

#ローマ字ひらがな変換表を読み込む
def setup_romaji_map_from_resource_name(resource_name):
    with open(resource_name, 'r', encoding='utf-8') as file:
        csv_data = csv.reader(file) #csvファイルを読み込む
        for line in csv_data: #csvファイルの各行について
            if len(line) == 2: #行の要素数が2なら
                romaji = line[0]
                kana = line[1]
                data = [kana, '0'] #ローマ字に対応するデータに[{ひらがな}, 0]を代入。0は移動量
            elif len(line) == 3: #行の要素数が3なら
                romaji = line[0]
                kana = line[1]
                offset = line[2] #行の3番目の要素を移動量とする
                try:
                    int(offset) #移動量が整数であることを確認
                except ValueError:
                    print(f"{resource_name}の{line}行目は不正です。")
                    continue
                data = [kana, offset] #ローマ字に対応するデータに[{ひらがな}, {移動量}]を代入
            else: #行の要素数が2でも3でもないなら
                if line != []: #空行でないならエラーを表示
                    print(f"{resource_name}の{line}行目は不正です。")
                continue
            romaji_to_japanese_map[romaji] = data #ローマ字をキーとして、ローマ字に対応するデータを代入

#ローマ字ひらがな変換表を読み込む
setup_romaji_map_from_resource_name(path.join(path.dirname(__file__), "romaji_to_hiragana.csv"))
setup_romaji_map_from_resource_name(path.join(path.dirname(__file__), "romaji_to_hiragana_2.csv"))

#ローマ字をひらがなに変換する関数
def convert_romaji_to_hiragana(romaji): #ローマ字をひらがなに変換する関数
    romaji = romaji.lower() #ローマ字を小文字に変換
    result = [] #結果を格納するリスト
    i = 0 #処理しているローマ字のインデックス（何文字目かから1引いた数、１文字目は0）
    while i < len(romaji): #変換する文字列の長さだけ繰り返す
        found = False #該当するローマ字が見つかったかどうかを表す変数
        for j in range(4, 0, -1): #4, 3, 2, 1の順にjを取る、多分総当り
            if i + j <= len(romaji): #処理しようとする文字数がローマ字文字列の長さ以下なら
                substring = romaji[i:i + j] #処理しようとする文字列を取得
                if substring in romaji_to_japanese_map: #処理しようとする文字列がローマ字変換表のキーにあるなら 
                    result.append(romaji_to_japanese_map[substring][0]) #結果のリストに変換後のひらがなを追加
                    i += j + int(romaji_to_japanese_map[substring][1]) #処理している文字列に処理した量足して辞書の移動量を足す(多分負の数)
                    found = True #該当するローマ字が見つかったことを表す変数をTrueにする
                    break
        else: #該当するローマ字が見つからなかったら
            result.append(romaji[i]) #変換しない
            i += 1 #インデックスを1増やす
    return ''.join(result) #結果のリストを文字列に変換して返す

#ひらがなを漢字に変換する関数
def transliterate_hiragana_to_kanji(hiragana_text):
    #パラメータを作成
    parameters = {
        'langpair': 'ja-Hira|ja',
        'text': hiragana_text
    }
    # GETリクエストを送信してレスポンスを取得
    response = requests.get('http://www.google.com/transliterate', params=parameters)
    response_json = response.json()
    # 変換結果を取得
    result = []
    for text in response_json: #結果のリストの各要素について（各要素は分割された入力文）
        processed_text = text[1][0] #変換された文字列を取得
        result.append(processed_text)
    #リストを文字列にする
    result = ''.join(result)
    if result == "":
        result = hiragana_text
    return result

#botが起動したときの処理
@bot.event
async def on_ready():
    print("botが起動しました")

#メッセージを受け取ったときの処理
@bot.event
async def on_message(message):
    if message.author.bot: #メッセージの送信者がbotなら
        #print("botからのメッセージを受け取りました")
        return
    
    text = message.content #メッセージの内容を取得
    if text.startswith(";") and text.endswith(";"): #絵文字に変換する場合
        text = text[1:-1]
        #print(text)
        #await message.channel.send(file=discord.File(temp_file))
        webhook = await check_webhook(message.channel)
        if not webhook:
            return
        text = text_processer(text) #テキストを処理
        #print("絵文字にするテキスト: " + text)
        #ランダムな色を生成
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        #print(type(color))
        img = create_emoji(text, color) #絵文字を生成
        img.save(temp_file)
        if type(message.channel) == discord.Thread: #スレッドなら
        #print("スレッドです")    
            await webhook.send(username=message.author.display_name, avatar_url=message.author.display_avatar, file=discord.File(temp_file), thread=message.channel)   
        else:
            await webhook.send(username=message.author.display_name, avatar_url=message.author.display_avatar, file=discord.File(temp_file))
        await message.delete()
    
    if text == "D" or text == "de": #絵文字を削除する場合
        #print("テキストはDかdeです")
        if message.reference: #メッセージへの返信なら
            #print("メッセージへの返信です")
            replied_message = await message.channel.fetch_message(message.reference.message_id) #返信先のメッセージを取得
            webhook = await check_webhook(message.channel) #webhookの情報を取得
            if not webhook:
                return
            #print(replied_message.webhook_id)
            #print(webhook.id)
            if replied_message.webhook_id == webhook.id: #メッセージを送信したwebhookがbotのwebhookなら
                #print("メッセージを送信したwebhookがbotのwebhookです")
                await replied_message.delete()
                await message.delete()
    
    #await bot.process_commands(message) #コマンドを処理する

#直接絵文字を作成するコマンド
@bot.slash_command(name="emoji", description="手動でテキストの絵文字を作成します。")
async def EMOJI(ctx, text: str, r: int = None, g: int = None, b: int = None):
    if r == None and g == None and b == None:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
    elif r == None or g == None or b == None:
        if r == None:
            r = 0
        if g == None:
            g = 0
        if b == None:
            b = 0
    webhook = await check_webhook(ctx.channel)
    if not webhook:
            await ctx.respond("このチャンネルではカスタム絵文字を使用できません。", ephemeral=True)
    #print("絵文字にするテキスト: " + text)
    color = (r, g, b)
    img = create_emoji(text, color) #絵文字を生成
    img.save(temp_file)
    if type(ctx.channel) == discord.Thread:
        await webhook.send(username=ctx.author.display_name, avatar_url=ctx.author.display_avatar, file=discord.File(temp_file), thread=ctx.channel)
    else:
        await webhook.send(username=ctx.author.display_name, avatar_url=ctx.author.display_avatar, file=discord.File(temp_file))
        await ctx.respond("絵文字を作成しました", ephemeral=True)


#ヘルプコマンド
@bot.slash_command(name="help", description="絵文字botのヘルプを表示します。")
async def HELP(ctx):
    #helpメッセージを作成
    embed = discord.Embed(title="絵文字botの使い方", description=help_message, url="https://github.com/daizu-007/aut_emojis_bot")
    await ctx.respond(embed=embed)

#テキストを絵文字用に変換する関数
def text_processer(text):
    text = convert_romaji_to_hiragana(text) #ローマ字をひらがなに変換
    if len(text) > 54: #テキストが54文字より長いなら
        text_list = split_text(text) #54字ごとに分割。google CGI APIの制限
        text = ""
        for translating_text in text_list:
            translated_text = transliterate_hiragana_to_kanji(translating_text) #ひらがなを漢字に変換
            text += translated_text
    else: #テキストが54文字以下なら
        text = transliterate_hiragana_to_kanji(text) #ひらがなを漢字に変換
    return text

#絵文字を生成する関数
def create_emoji(text, color):
    #透明な画像を作成
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    #描画オブジェクトを作成
    #draw = ImageDraw.Draw(img)
    #字数等を計算
    lenge = len(text) #テキストの長さ
    lenge_sqrt = math.sqrt(lenge) #テキストの長さの平方根
    horizontal_lenge = math.ceil(lenge_sqrt) #横の文字数
    vertical_lenge = math.ceil(lenge / horizontal_lenge) #縦の文字数
    char_width = size / horizontal_lenge #一文字の横幅
    char_height = size / vertical_lenge #一文字の縦幅
    #print("horizontal_lenge=" + str(horizontal_lenge))
    #print("vertical_lenge=" + str(vertical_lenge))
    #print("--------------------------------------------------")
    #一文字ずつ処理する
    for i in range(lenge):
        char = text[i]
        number = i + 1
        #画像にする
        char_img = text_to_image(char, color)
        #画像をリサイズする
        char_img = char_img.resize((int(char_width), int(char_height)))
        #画像を貼り付ける位置を計算する
        if number % horizontal_lenge == 0: #一番右側なら
            x = ((horizontal_lenge - 1) * char_width)# + (char_width / 2)
            y = (((number // horizontal_lenge) - 1) * char_height)# + (char_height / 2)
            #print("it's right edge")
        else:
            x = (((number % horizontal_lenge) - 1) * char_width)# + (char_width / 2)
            y = ((number // horizontal_lenge) * char_height)# + (char_height / 2)
            #print("it's not right edge")
        #画像を貼り付ける
        img.paste(char_img, (int(x), int(y)))
        
        #デバッグ用
        """
        print("number=" + str(number))
        print("text=" + char)
        print("char_width=" + str(char_width))
        print("char_height=" + str(char_height))
        print("x=" + str(x))
        print("y=" + str(y))
        print("--------------------------------------------------")
        """
    #画像を返す
    return img

#渡された文字を正方形の画像にする関数
def text_to_image(char,color=(0,0,0,255)):
    #透明な画像を作成
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    #描画オブジェクトを作成
    draw = ImageDraw.Draw(img)
    #フォントの大きさを調節
    font_size = 1
    font = ImageFont.truetype(font_path, font_size)
    size_of_font = font.getbbox(char)
    while max(size_of_font[2],size_of_font[3]) < size:
        font_size += 1
        font = ImageFont.truetype(font_path, font_size)
        size_of_font = font.getbbox(char)
    font = ImageFont.truetype(font_path, font_size + 20)
    #画像に文字を描画する
    draw.text((size//2, size//2), char, font=font, fill=color, anchor="mm")
    #画像を返す
    return img

#テキストを形態素解析して分割する関数
def split_text(text):
    count_limit = 54
    splited_text = gooAPI.morph(sentence=text, info_filter="form")["word_list"][0] #形態素解析
    result = []
    while splited_text: #splited_textが空になるまで続ける
        block = ""
        if len(block)+len(splited_text[0]) < count_limit:
            while len(block)+len(splited_text[0]) < count_limit: #blockにsplited_textの最初の単語を追加してもcount_limitを超えない間続ける
                block += splited_text.pop(0)[0] #splited_textの最初の単語をblockに追加して削除
                if not splited_text: #splited_textが空になったらwhileを抜ける
                    break
        else:
            block += splited_text.pop(0)[0]
        result.append(block)
    return result

#webhookの存在確認及び作成関数
async def check_webhook(channel):
    try:

        if type(channel) == discord.TextChannel or type(channel) == discord.ForumChannel:
            webhooks = await channel.webhooks() #webhookの情報を取得
            processed_webhooks = [obj for obj in webhooks if obj.name == "bot"]#webhookの情報からbotのwebhookの情報を取得
            if processed_webhooks:
                webhook = processed_webhooks[0] #botのwebhookの情報を取得
            else:
                webhook = await channel.create_webhook(name="bot") #botのwebhookを作成
            return webhook
        elif type(channel) == discord.Thread:
            thread_parent = channel.parent
            webhook = await check_webhook(thread_parent) #threadの親チャンネルのwebhookを取得
            return webhook       
        else:
            print(f"{type(channel)}ではwebhookを使用できません。")
            return None
        
    except Exception as e:
        print("webhookの確認に失敗しました")
        print(e)
        return None

#実行時に実行される処理
if __name__ == "__main__":
    print("botを実行します")
    try:

        bot.run(token) #botを実行

    except Exception as e:
        print("botの実行に失敗しました")
        print(e)
        

#テスト
#img = create_emoji("おはらぎ")
#img = text_to_image("お")
#img.save("C:/my projects/python/discord bots/aut_emojis_bot/test_images/test.png")
#print(text_processer("korehakeitaisobunnsekiwofukumutekisutosyorizenntainotesutonotamenitukuraretabunnsyoudesu.monosugoityoubunnnitaisitedonoyounisyorisurunokakininarunodesugaro-majidetyoubunnwosakuseisurunohanakanakataihennnasagyoudesu.imanagareteiruonngakuhannanndesyouka?robottoda-tteitteimasune.sirabetemimasyouka?dannsurobottodannsutoiukyokurasiidesu.sorosorozisuutekinityoudoiidesukane?dounanndesyouka?"))


"""メモ

"""