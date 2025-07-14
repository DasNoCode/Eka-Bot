from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message
import re


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "unban",
                "category": "owner",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": True,
                "ChatOnly": False,
                "description": {
                    "content": "unban a user from using the bot",
                    "usage": "/unban @username [reason] \n\nExamples:\n/unban @toxic_user Being annoying \nReply to a user's message with /unban to unban them directly."
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
                message.chat_id, f"@{message.sender.user_name}, please mention or reply to a user to unban them!"
            )

        if target_user_id == self.client.bot_id or target_user_id == self.client.owner_id:
            return await self.client.send_message(
                message.chat_id, f"@{message.sender.user_name}, you can't unban me nor the owner !"
            )


        self.client.db.User.update_ban(target_user_id, False)

        await self.client.send_message(
            message.chat_id,
            f"Successfully **unbanned** @{target_username} from using @{message.bot_username}",
        )
