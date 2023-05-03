# coding=utf-8
from game import Game
from games import Ito, WordWolf

import discord
import json

# config.jsonの読み込み
with open("config.json", "r") as f:
    conf = json.load(f)
client = discord.Client()

game = Game()


@client.event
async def on_ready():
    print("Tenka > I wake up!")


@client.event
async def on_message(message):
    global game
    # メッセージの受信時に呼び出される
    if message.author.bot:
        return
    print(f"Game: {game.name}")

    msg = message.content

    if msg == "$gameend":
        game = Game()
        await message.channel.send("End game")
        return

    exist = False
    if isinstance(message.channel, discord.channel.DMChannel):
        exist = await game.on_direct_message(message)
    else:
        exist = await game.on_group_message(message)

    if exist:
        # Gameオブジェクト側でon_message処理が成功していれば終了
        return

    if msg.startswith("$"):
        command = msg[1:]
        if command.startswith("start "):
            gname = command[6:]
            if gname == "ito":
                game = Ito()
                await message.channel.send("Start ito")
                print(f"Game: {game.name}")
            if gname == "wordwolf":
                game = WordWolf()
                await message.channel.send("Start wordwolf")
                print(f"Game: {game.name}")


@client.event
async def on_voice_state_update(member, before, after):
    # Voiceの状況が変わったときに呼び出される
    # チャンネル移動やミュートの解除など
    pass

token = conf["token"]
client.run(token)
