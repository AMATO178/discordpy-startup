from discord.ext import commands
import os
import traceback
import discord
import sys

# さいころの和を計算する用の関数
from func import  diceroll

TOKEN = '任意のトークン'

# client = discord.Client()
bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

@bot.event
async def on_ready():
    print('--------------')
    print('ログインしました')
    print(bot.user.name)
    print(bot.user.id)
    print('--------------')
    channel = bot.get_channel('チャンネルID')
    await channel.send('楽しいTRPGを始めましょう！')
    
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith("!dice"):
        # 入力された内容を受け取る
        say = message.content 

        # [!dice ]部分を消し、AdBのdで区切ってリスト化する
        order = say.strip('!dice ')
        cnt, mx = list(map(int, order.split('d'))) # さいころの個数と面数
        dice = diceroll(cnt, mx) # 和を計算する関数(後述)
        await message.channel.send(dice[cnt])
        del dice[cnt]

        # さいころの目の総和の内訳を表示する
        await message.channel.send(dice)
        
@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def neko(ctx):
    await ctx.send('にゃーん')


bot.run(token)


func.py
import random

def diceroll(cnt, max):
    total = 0
    num_list = []
    for i in range(0, cnt):
        # ランダムに1からサイコロの面数までの和を取得しリストに入れる
        num = random.randint(1, max)
        num_list.append(num)
    # さいころの目の総和を計算しリストに入れる
    total = sum(num_list)
    num_list.append(total)
    return num_list
