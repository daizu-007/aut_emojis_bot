#絵文字を自動生成するdiscord bot

import discord
import PIL

intents = discord.Intents.all()
bot = discord.Bot(intents=intents, command_prefix="/")

