#絵文字を自動生成するdiscord bot

#import discord
from PIL import Image, ImageDraw, ImageFont
import json
from os import path
import random
import math
import textwrap

#あとから変更するかもしれない変数
size = 128 #画像のサイズ

#intents = discord.Intents.all()
#bot = discord.Bot(intents=intents, command_prefix="/")

#config.jsonから設定を読み込む
with open(path.join(path.dirname(__file__), "config.json"), "r") as f:
    config = json.load(f)
token = config["token"]
font_path = config["font_path"]
"""
#botが起動したときの処理
@bot.event
async def on_ready():
    print("botが起動しました")

#メッセージを受け取ったときの処理
@bot.event
async def on_message(message):
    text = message.content #メッセージの内容を取得
    if text.startswith("?"):
        text = text[1:]
"""
#絵文字を生成する関数
def create_emoji(text):
    #ランダムな色を生成
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    #透明な画像を作成
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    #描画オブジェクトを作成
    draw = ImageDraw.Draw(img)
    #字数等を計算
    lenge = len(text) #テキストの長さ
    lenge_sqrt = math.sqrt(lenge) #テキストの長さの平方根
    horizontal_lenge = math.ceil(lenge_sqrt) #横の文字数
    vertical_lenge = math.ceil(lenge / horizontal_lenge) #縦の文字数
    char_width = size / horizontal_lenge #一文字の横幅
    char_height = size / vertical_lenge #一文字の縦幅
    #一文字ずつ処理する
    for i in range(lenge):
        char = text[i]
        #画像にする
        char_img = text_to_image(char, color)
        #画像をリサイズする
        char_img = char_img.resize((char_width, char_height))
        #画像を貼り付ける位置を計算する
        if i % horizontal_lenge == 0: #一番右側なら
            x = ((horizontal_lenge - 1) * char_width) + (char_width / 2)
        else:
            x = (((i % horizontal_lenge) - 1) * char_width) + (char_width / 2)
        y = ((i // horizontal_lenge) * char_height) + (char_height / 2) #TODO AI生成、未検証、後で確認
    

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
    #画像に文字を描画する
    draw.text((size//2, size//2), char, font=font, fill=color, anchor="mm")
    #画像を返す
    return img

#テスト
#img = create_emoji("おやすらぎ…")
#img = text_to_image("お")
#img.show()


"""メモ

"""