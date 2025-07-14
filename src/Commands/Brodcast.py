from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "brodcast", 
                "category": "owner",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": True,
                "ChatOnly": False,
                "description": {
                    "content": "Broadcast a message to all chats where the bot is present.",
                    "usage": "Reply to a message and use /brodcast to send it to all chats.\n\nExample:\n/brodcast (as a reply to a message)"
                },
            },
        )

    async def exec(self, message: Message, context):
        chat_data = self.client.db.Chat.get_all_chat_datas()
        user_data = self.client.db.User.get_all_users()

        if not message.reply_to_message or not message.reply_to_message.text:
            return await self.client.send_message(
                message.chat_id, "❌ Please reply to a text message to broadcast it."
            )

        broadcast_text = message.reply_to_message.text

        for target_chat_id in chat_data:
            await self.client.send_message(
                target_chat_id.get("chat_id"), f"**📣 BROADCAST MESSAGE**\n\n{broadcast_text}"
            )
        for target_chat_id in user_data:
            if target_chat_id.get("user_id"):
                await self.client.send_message(
                    target_chat_id.get("user_id"), f"**📣 BROADCAST MESSAGE**\n\n{broadcast_text}"
                )