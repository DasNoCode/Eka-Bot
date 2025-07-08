from pyrogram.types import ChatPrivileges

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "demote",
                "category": "chat",
                "xp": False,
                "AdminOnly": True,
                "OwnerOnly": False,
                "ChatOnly": True,
                "description": {
                    "content": "Demotes a user from admin to regular member in the chat.",
                    "usage": "/demote @username\nor\nReply to the user’s message with /demote"
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
                message.chat_id,
                f"@{message.sender.user_name}, please reply to or mention a user to **demote**.",
            )

        await self.client.promote_chat_member(
            message.chat_id,
            target_user.user_id,
            ChatPrivileges(
                can_change_info=False,
                can_invite_users=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_video_chats=False,
                is_anonymous=False,
            ),
        )

        await self.client.send_message(
            message.chat_id,
            f"Successfully **demoted** @{target_user.user_name} to a regular member in **{message.chat_title}**.",
        )
