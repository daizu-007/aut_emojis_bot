#絵文字を自動生成するdiscord bot

import discord
from PIL import Image, ImageDraw, ImageFont
import json
from os import path
import random
import math
#import textwrap

#あとから変更するかもしれない変数
size = 128 #画像のサイズ

temp_file = __file__[:-6] + "temp\emoji.png"
print(temp_file)
intents = discord.Intents.all()
intents.messages = True
bot = discord.Bot(intents=intents, command_prefix="/")

#config.jsonから設定を読み込む
with open(path.join(path.dirname(__file__), "config.json"), "r") as f:
    config = json.load(f)
token = config["token"]
font_path = config["font_path"]

#botが起動したときの処理
@bot.event
async def on_ready():
    print("botが起動しました")

#メッセージを受け取ったときの処理
@bot.event
async def on_message(message):
    if message.author.bot: #メッセージの送信者がbotなら
        return
    text = message.content #メッセージの内容を取得
    if text.startswith(";") and text.endswith(";"):
        text = text[1:-1]
        print(text)
        #await message.channel.send(file=discord.File(temp_file))
        if type(message.channel) == discord.TextChannel:
            webhooks = await message.channel.webhooks() #webhookの情報を取得
            processed_webhooks = [obj for obj in webhooks if obj.name == "daizu-bot"]#webhookの情報からbotのwebhookの情報を取得
        else:
            processed_webhooks = []
        if processed_webhooks:
            webhook = processed_webhooks[0] #botのwebhookの情報を取得
            img = create_emoji(text) #絵文字を生成
            img.save(temp_file)
            await webhook.send(username=message.author.display_name, avatar_url=message.author.display_avatar, file=discord.File(temp_file))
            await message.delete()
        else:
            await message.reply("このチャンネルにはbotのwebhookがありません")

#絵文字を生成する関数
def create_emoji(text):
    #ランダムな色を生成
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
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

#実行時に実行される処理
if __name__ == "__main__":
    bot.run(token) #botを実行

#テスト
#img = create_emoji("おはらぎ")
#img = text_to_image("お")
#img.save("C:/my projects/python/discord bots/aut_emojis_bot/test_images/test.png")


"""メモ

"""