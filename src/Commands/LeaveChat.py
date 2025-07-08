from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "leave",
                "category": "owner",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": True,
                "ChatOnly": True,
                "description": {
                    "content": "Make the bot leave the chat (Owner only).",
                    "usage": "/leave — Bot will leave the current group. Only works for the bot owner."
                },
            },
        )

    async def exec(self, M: Message, context):
        if self.client.owner_id != M.sender.user_id:
            return await self.client.send_message(
                M.chat_id,
                f"@{M.sender.user_name}, you don't have permission to use this command!"
            )

        await self.client.send_message(M.chat_id, "Thanks for everything — see you around!")
        await self.client.db.Chat.delete_chat(M.chat_id)
        await self.client.leave_chat(M.chat_id, delete=True)
