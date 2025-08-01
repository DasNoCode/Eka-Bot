from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message
import re


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "ban",
                "category": "owner",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": True,
                "ChatOnly": False,
                "description": {
                    "content": "Ban a user from using the bot. Can be used with an optional reason and ban duration.",
                    "usage": "/ban @username [reason] [time=duration]\n\nExamples:\n/ban @toxic_user Being annoying time=3days\nReply to a user's message with /ban to ban them directly."
                },
            },
        )

    async def exec(self, message: Message, context):
        if message.reply_to_message:
            target_username = message.reply_to_message.replied_user.user_name
            target_user_id = message.reply_to_message.replied_user.user_id
        elif message.mentioned:
            mentioned_user = message.mentioned[0]
            target_username = mentioned_user.user_name
            target_user_id = mentioned_user.user_id
        else:
            return await self.client.send_message(
                message.chat_id, f"@{message.sender.user_name}, please mention or reply to a user to ban them!"
            )

        if target_user_id == self.client.bot_id or target_user_id == self.client.owner_id:
            return await self.client.send_message(
                message.chat_id, f"@{message.sender.user_name}, you can't ban me nor the owner !"
            )

        ban_data = self.client.db.User.get_user(user_id=target_user_id).get("ban")
        if ban_data.get("is_ban"):
            return await self.client.send_message(
                message.chat_id, f"@{message.sender.user_name}, this user is already **banned!**"
            )

        combined_text = context[1]
        for word in ["/ban", f"@{target_username}"]:
            combined_text = combined_text.replace(word, "")
        self.client.db.User.update_ban(target_user_id, True, combined_text)

        await self.client.send_message(
            message.chat_id,
            f"Successfully **banned** @{target_username} from using @{message.bot_username}",
        )
