from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "kick",
                "category": "chat",
                "xp": False,
                "AdminOnly": True,
                "OwnerOnly": False,
                "ChatOnly": True,
                "description": {
                    "content": "Kick a user from the chat temporarily (soft ban).",
                    "usage": "/kick [mention/reply] — kicks the user from the group."
                },
            },
        )

    async def exec(self, M: Message, context):
        if M.reply_to_message:
            target_user = M.reply_to_message.replied_user
        elif M.mentioned:
            target_user = M.mentioned[0]
        else:
            return await self.client.send_message(
                M.chat_id,
                f"@{M.sender.user_name}, please reply to or mention a user to ban."
            )

        user_id = target_user.user_id
        user_name = target_user.user_name

        await self.client.ban_chat_member(M.chat_id, user_id)
        await self.client.send_message(
            M.chat_id,
            f"🚫 Successfully **kicked** @{user_name} from **{M.chat_title}**"
        )
        await self.client.unban_chat_member(M.chat_id, user_id)
