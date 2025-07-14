from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "senddb",
                "category": "owner",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": True,
                "ChatOnly": False,
                "description": {
                    "content": "Say hello to the bot and get a friendly greeting.",
                    "usage": "/hi — The bot will greet you back!"
                },
            },
        )

    async def exec(self, M: Message, context):
        return await self.client.send_animation(M.chat_id, self.client.utils.get_tenor_gif_urls("you won")[0])
        for jsondb in ["ChatDatabse.json","UserDatabse.json"]:
         await self.client.send_document(M.chat_id, jsondb)