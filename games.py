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
        elif msg.startswith("hand"):
            splitted_msg = msg.split()
            if len(splitted_msg) <= 1:
                await message.channel.send("複数枚配る場合は `hand [枚数]` と入力してください! [Length error]")
            try:
                i = int(splitted_msg[1])
                if len(self.players) * i > 100:
                    await message.channel.send("人数が多すぎます!")
                nums = [i for i in range(1, 101)]
                random.shuffle(nums)
                for k in self.players:
                    card = []
                    for _ in range(i):
                        card.append(str(nums.pop()))
                    self.players[k] = ", ".join(card)
                    await self.notify(k)
            except ValueError:
                await message.channel.send("複数枚配る場合は `hand [枚数]` と入力してください! [Value error]")
        return True

    async def notify(self, ch):
        if self.players[ch]:
            await ch.send(f"あなたの番号は{self.players[ch]}です。")
        else:
            await ch.send("番号が割り振られていません。")


class WordWolf(Game):
    def __init__(self):
        self.name = "wordwolf"
        self.players = {}
        self.wolf = ""
        self.THEMES = [
            "楽しい",
            "嬉しい",
            "悲しい",
            "葬式で流れていそう",
            "朝っぽい",
            "昼っぽい",
            "夜っぽい",
            "幸せな",
            "面白い",
            "晴れやか",
            "苦しい",
            "怖い",
            "寂しい",
            "憂鬱",
            "億劫な"]

    async def on_direct_message(self, message):
        print(f"DM: {message.author} > {message.content}")
        msg = message.content
        if msg == "join":
            if message.channel in self.players:
                await message.channel.send("もう入っています!")
            else:
                self.players[message.channel] = ""
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
            themes = random.sample(self.THEMES, 2)
            minor = random.randrange(len(self.players))
            cnt = 0
            members = []
            for k in self.players:
                members.append(k.recipient.name)
                if cnt == minor:
                    self.players[k] = themes[1]
                    self.wolf = k.recipient.name
                else:
                    self.players[k] = themes[0]
                cnt += 1
                await self.notify(k)
            random.shuffle(members)
            await message.channel.send("->".join(members))
        elif msg == "answer":
            await message.channel.send(f"ウルフは{self.wolf}でした！")
        return True

    async def notify(self, ch):
        if self.players[ch]:
            await ch.send(f"あなたのテーマは「{self.players[ch]}」です。")
        else:
            await ch.send("テーマが割り振られていません。")
