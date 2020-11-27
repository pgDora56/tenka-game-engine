class Game:
    # Abstract class
    def __init__(self):
        self.name = ""

    async def on_direct_message(self, message):
        print("Null DM")
        return False

    async def on_group_message(self, message):
        print("Null GM")
        return False
