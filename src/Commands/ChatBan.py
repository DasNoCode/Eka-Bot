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
                "ChatOnly" : True,
                "description": {"content": "Prevents bots by verifying new users with a captcha challenge."},
            },
        )

    async def exec(self, M: Message, context):

        if M.reply_to_message:
            user_name = M.M.reply_to_message.replied_user.user_name
            user_id = M.M.reply_to_message.replied_user.user_id
        elif M.mentioned:
            usermentioned_user = M.mentioned[0]
            user_name = usermentioned_user.user_name
            user_id = usermentioned_user.user_id

        await self.client.ban_chat_member(M.chat_id, user_id)
        await self.client.send_message(
            M.chat_id,
            f"Successfully banned @{user_name} from {M.chat_title}",
        )