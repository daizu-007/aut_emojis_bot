#絵文字を自動生成するdiscord bot

#import discord
from PIL import Image, ImageDraw, ImageFont
import json
from os import path
import random
import math
import textwrap

#intents = discord.Intents.all()
#bot = discord.Bot(intents=intents, command_prefix="/")
font_path = path.dirname(__file__) + '\\NotoSansJP-Bold.ttf'
font = ImageFont.truetype(font_path, 140)

#keys.jsonからトークンを読み込む
with open(path.join(path.dirname(__file__), "keys.json"), "r") as f:
    keys = json.load(f)
token = keys["token"]
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
    #テキストを字数に応じて改行する
    lenge = len(text) #テキストの長さ
    lenge_sqrt = math.sqrt(lenge) #テキストの長さの平方根
    words = math.ceil(lenge_sqrt) #平方根の切り上げ
    prossesed_text = textwrap.fill(text, words)
    #透明な画像を作成
    img = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    #ランダムな色を生成
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    #画像に文字を描画する
    draw = ImageDraw.Draw(img)
    draw.multiline_text((0, 0), prossesed_text, font=font, fill=(r, g, b, 255), align="center")
    #画像を返す
    return img

#テスト
img = create_emoji("おやすらぎ…")
img.show()