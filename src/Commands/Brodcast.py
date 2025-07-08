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
        chat_data = self.client.db.Chat.get_chat_data(message.chat_id)

        if not message.reply_to_message or not message.reply_to_message.text:
            return await self.client.send_message(
                message.chat_id, "❌ Please reply to a text message to broadcast it."
            )

        broadcast_text = message.reply_to_message.text

        for target_chat_id in chat_data.get("chat_id"):
            await self.client.send_message(
                target_chat_id, f"**📣 BROADCAST MESSAGE**\n\n{broadcast_text}"
            )
