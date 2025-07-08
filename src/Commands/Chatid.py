from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "chatid",
                "category": "chat",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": False,
                "ChatOnly": True,
                "exp": 1,
                "description": {
                    "content": "Returns the unique ID of the current chat.",
                    "usage": "/chatid\n\nShows the Telegram chat ID where the command is used."
                },
            },
        )

    async def exec(self, message: Message, context):
        await self.client.send_message(
            message.chat_id, f"**Chat ID:** `{message.chat_id}`"
        )
