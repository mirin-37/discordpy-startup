import discord
import asyncio
import re
import sys
import random
import os
import traceback

from discord.ext import commands
from discord.ext import tasks
from googlesearch import search

CHANNEL_ID = 629698076646309890 #ログオフ、ログオンメッセージ用のチャンネルID
KAIWA_ID = 633909382501105674 #リブラと会話用のチャンネルID

client = discord.Client()

ModeFlag = 0


bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(str(error))


#@bot.command()
#async def ping(ctx):
#    await ctx.send('pong')

@client.event
async def on_ready():
    # 起動時にメッセージの送信
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('リブラ、準備完了です！')

@client.event
async def on_message(message):

    global ModeFlag

    if message.author.bot:
        return

    if client.user in message.mentions:
        if message.channel.id == KAIWA_ID:
            reply = message.author.mention + "さん、お呼びですか？\nGoogle検索　　：「リブラ、Google」または「!Google」\nサイコロを振る：「リブラ、サイコロ」または「!Dice」\nです"
            await message.channel.send(reply)
        else:
            reply = message.author.mention + "さん、お呼びですか？\nよろしければ「リブラと会話する部屋」までお越しください"
            await message.channel.send(reply)



    if re.fullmatch("!Sleep", message.content):
        channel = client.get_channel(CHANNEL_ID)
        await channel.send('休憩のご指示を受けましたので、休憩してきますね！')
        await client.logout()
        await sys.exit()

    if re.fullmatch("リブラ、おやすみ", message.content):
        channel = client.get_channel(CHANNEL_ID)
        await channel.send('休憩のご指示を受けましたので、休憩してきますね！')
        await client.logout()
        await sys.exit()


    if ModeFlag == 1:
        if message.channel.id == KAIWA_ID:
            kensaku = message.content
            ModeFlag = 0
            count = 0

            if kensaku == "!Cancel":
                await message.channel.send('Google検索をキャンセルしました')
                return
            elif kensaku == "リブラ、キャンセル":
                await message.channel.send('Google検索をキャンセルしました')
                return
            elif kensaku == "!Dice":
                await message.channel.send('Google検索をキャンセルしました')
            elif kensaku == "リブラ、サイコロ":
                await message.channel.send('Google検索をキャンセルしました')
            elif kensaku == "!Sleep":
                await message.channel.send('Google検索をキャンセルしました\n休憩に入ります！')
            elif kensaku == "リブラ、おやすみ":
                await message.channel.send('Google検索をキャンセルしました\n休憩に入ります！')
            elif kensaku == "リブラ、Google":
                await message.channel.send('Google検索の指示を2重に受けているため、最初の指示をキャンセルしました')
            elif kensaku == "!Google":
                await message.channel.send('Google検索の指示を2重に受けているため、最初の指示をキャンセルしました')

            else:
                for url in search(kensaku, lang="jp", num = 3):
                    await message.channel.send(url)
                    count += 1
                    if(count == 3):
                        await message.channel.send('こんなのが検索できましたよ！')
                        break
        else:
            channel = client.get_channel(KAIWA_ID)
            ModeFlag = 0
            await channel.send('他のチャンネルで発言があったため、Google検索を中止しました\n申し訳ありませんが再度Google検索を実行してください')
            await message.channel.send('Google検索を実行中の方がいます\nその方と調整の上、出来れば発言タイミングをずらしていただけると助かります')
            return



    if re.fullmatch("!Dice", message.content):
        if message.channel.id == KAIWA_ID:
            num_random = random.randrange(1,6)
            num_dice = str(num_random)
            await message.channel.send('サイコロを振ります。\n出た目の数は… ' + num_dice + ' ですよ！')
        else:
            await message.channel.send('申し訳ありません、サイコロが「リブラと会話する部屋」にしかありません')
            return
    elif re.fullmatch('リブラ、サイコロ', message.content):
        if message.channel.id == KAIWA_ID:
            num_random = random.randrange(1,6)
            num_dice = str(num_random)
            await message.channel.send('サイコロを振ります。\n出た目の数は… ' + num_dice + ' ですよ！')
        else:
            await message.channel.send('申し訳ありません、サイコロが「リブラと会話する部屋」にしかありません')
            return
    elif re.fullmatch('!Google', message.content):
        if message.channel.id == KAIWA_ID:
            ModeFlag = 1
            await message.channel.send('Googleで検索したいワードをチャットで発言してね\nキャンセルしたい場合は「リブラ、キャンセル」または「!Cancel」と発言してください')
        else:
            await message.channel.send('申し訳ありません、Google検索は「リブラと会話する部屋」でしか使えません')
            return
    elif re.fullmatch('リブラ、Google', message.content):
        if message.channel.id == KAIWA_ID:
            ModeFlag = 1
            await message.channel.send('Googleで検索したいワードをチャットで発言してね\nキャンセルしたい場合は「リブラ、キャンセル」または「!Cancel」と発言してください')
        else:
            await message.channel.send('申し訳ありません、Google検索は「リブラと会話する部屋」でしか使えません')
            return
    elif message.content.startswith("おはよう"):
        if message.channel.id == KAIWA_ID:
            m = "おはよう、" + message.author.name + "さん！"
            if message.author.bot:
                return
            await message.channel.send(m)

    elif message.content.startswith("おはよー"):
        if message.channel.id == KAIWA_ID:
            m = "おはよう、" + message.author.name + "さん！"
            if message.author.bot:
                return
            await message.channel.send(m)

    elif message.content.startswith("おはよ～"):
        if message.channel.id == KAIWA_ID:
            m = "おはよう、" + message.author.name + "さん！"
            if message.author.bot:
                return
            await message.channel.send(m)

    elif message.content.startswith("おっはー"):
        if message.channel.id == KAIWA_ID:
            m = "おはよう、" + message.author.name + "さん！"
            if message.author.bot:
                return
            await message.channel.send(m)

    elif message.content.startswith("おっは～"):
        if message.channel.id == KAIWA_ID:
            m = "おはよう、" + message.author.name + "さん！"
            if message.author.bot:
                return
            await message.channel.send(m)

    elif message.content.startswith("OHAYO"):
        if message.channel.id == KAIWA_ID:
            m = "おはよう、" + message.author.name + "さん！"
            if message.author.bot:
                return
            await message.channel.send(m)

    elif message.content.startswith("こんにちは"):
        if message.channel.id == KAIWA_ID:
            m = "こんにちは、" + message.author.name + "さん！"
            if message.author.bot:
                return
            await message.channel.send(m)

    elif message.content.startswith("こんばんは"):
        if message.channel.id == KAIWA_ID:
            m = "こんばんは、" + message.author.name + "さん！"
            if message.author.bot:
                return
            await message.channel.send(m)

    else:
        return


bot.run(token)
