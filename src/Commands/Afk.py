from datetime import datetime

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "afk",
                "category": "chat",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": False,
                "ChatOnly": True,
                "description": {
                    "content": "Mark yourself as AFK (Away From Keyboard). Other users will be notified when they mention you.",
                    "usage": "/afk [reason]\n\nExamples:\n/afk\n/afk Out for lunch"
                },
            },
        )

    async def exec(self, message: Message, context):
        current_time = datetime.now().time().strftime("%H:%M:%S")
        user_data = self.client.db.User.get_user(message.sender.user_id)

        if user_data["afk"]["is_afk"]:
            return await self.client.send_message(
                message.chat_id, f"@{message.sender.user_name}, you are already marked as AFK."
            )

        afk_reason = context[1] if context[1] else None
        self.client.db.User.set_afk(
            message.sender.user_id, True, afk_reason, current_time
        )

        await self.client.send_message(
            message.chat_id, f"@{message.sender.user_name} is now marked as AFK!"
        )
