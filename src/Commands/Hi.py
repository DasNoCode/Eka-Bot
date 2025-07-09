from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "hi",
                "category": "general",
                "xp": True,
                "AdminOnly": False,
                "OwnerOnly": False,
                "ChatOnly": False,
                "description": {
                    "content": "Say hello to the bot and get a friendly greeting.",
                    "usage": "/hi — The bot will greet you back!"
                },
            },
        )

    async def exec(self, M: Message, context):
        await self.client.send_message(
            M.chat_id,
            f"Hey @{M.sender.user_name}, how's your day going? Use `/help` to explore available commands!"
        )
