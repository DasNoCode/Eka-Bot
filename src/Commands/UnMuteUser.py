from pyrogram.types import ChatPermissions

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "unmute",
                "category": "chat",
                "xp": False,
                "AdminOnly": True,
                "OwnerOnly": False,
                "ChatOnly": True,
                "description": {
                    "content": "Unmute a previously muted user in the chat.",
                    "usage": "/unmute by replying to a user or mentioning them."
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
                f"@{M.sender.user_name}, reply to a user or mention a user to **unmute** them!"
            )

        user_id = target_user.user_id
        user_name = target_user.user_name

        permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_send_polls=True,
            can_invite_users=True,
            can_pin_messages=True,
            can_change_info=True
        )

        chat_data = self.client.db.Chat.get_chat_data(M.chat_id)
        mute_list = chat_data.get("moderation", {}).get("mute_list", [])

        if user_id in mute_list:
            mute_list.remove(user_id)
            self.client.db.Chat.update_chat_datas(
                M.chat_id, {"moderation": {"mute_list": mute_list}}
            )
            await self.client.send_message(
                M.chat_id,
                f"Successfully **unmuted** @{user_name} in {M.chat_title}."
            )
        else:
            await self.client.send_message(
                M.chat_id,
                f"@{user_name} is not muted in {M.chat_title}."
            )

        await self.client.restrict_chat_member(M.chat_id, user_id, permissions)
