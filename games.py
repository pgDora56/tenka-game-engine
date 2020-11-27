from game import Game
import random


class Ito(Game):
    def __init__(self):
        self.name = "ito"
        self.players = {}

    async def on_direct_message(self, message):
        print(f"DM: {message.author} > {message.content}")
        msg = message.content
        if msg == "join":
            if message.channel in self.players:
                await message.channel.send("もう入っています!")
            else:
                self.players[message.channel] = 0
                await message.channel.send("参加しました!")
        elif msg == "exit":
            if message.channel in self.players:
                del self.players[message.channel]
                await message.channel.send("退出しました。")
            else:
                await message.channel.send("そもそも参加してないよ!!")
        elif msg == "notify":
            if message.channel in self.players:
                await self.notify(message.channel)
            else:
                await message.channel.send("まずは参加してください!")
        return True

    async def on_group_message(self, message):
        print(f"GM: {message.author} in {message.channel} > {message.content}")
        if not message.content.startswith("$"):
            return True

        msg = message.content[1:]
        if msg == "member":
            if len(self.players) == 0:
                await message.channel.send("ひとりもいません。")
            else:
                members = []
                for plch in self.players:
                    members.append(plch.recipient.name)
                await message.channel.send(", ".join(members))
        elif msg == "hand":
            if len(self.players) > 100:
                await message.channel.send("人数が多すぎます!")
            nums = [i for i in range(1, 101)]
            random.shuffle(nums)
            for k in self.players:
                self.players[k] = nums.pop()
                await self.notify(k)
        return True

    async def notify(self, ch):
        if self.players[ch]:
            await ch.send(f"あなたの番号は{self.players[ch]}です。")
        else:
            await ch.send("番号が割り振られていません。")
