from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "chatban",
                "category": "chat",
                "xp": False,
                "AdminOnly": True,
                "OwnerOnly": False,
                "ChatOnly": True,
                "description": {
                    "content": "Ban a user from the current chat. Admins only.",
                    "usage": "/chatban @username\nor\nReply to a user's message with /chatban"
                },
            },
        )

    async def exec(self, message: Message, context):

        if message.reply_to_message:
            target_user = message.reply_to_message.replied_user
        elif message.mentioned:
            target_user = message.mentioned[0]
        else:
            return await self.client.send_message(
                message.chat_id, f"@{message.sender.user_name}, please reply to or mention a user to ban."
            )

        user_name = target_user.user_name
        user_id = target_user.user_id

        await self.client.ban_chat_member(message.chat_id, user_id)
        await self.client.send_message(
            message.chat_id,
            f"Successfully **banned** @{user_name} from {message.chat_title}.",
        )
