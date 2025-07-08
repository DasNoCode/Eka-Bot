from pyrogram.types import ChatPermissions

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "mute",
                "category": "chat",
                "xp": False,
                "AdminOnly": True,
                "OwnerOnly": False,
                "ChatOnly": True,
                "description": {
                    "content": "Mute a user in the chat, preventing them from sending any messages.",
                    "usage": "/mute @username or reply to a user's message to mute them."
                },
            },
        )

    async def exec(self, M: Message, context):
        if M.reply_to_message:
            user = M.reply_to_message.replied_user
        elif M.mentioned:
            user = M.mentioned[0]
        else:
            return await self.client.send_message(
                M.chat_id,
                f"@{M.sender.user_name}, please reply to a user or mention them to mute."
            )

        user_id = user.user_id
        user_name = user.user_name

        mute_permissions = ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False,
            can_send_polls=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_change_info=False,
        )

        chat_data = self.client.db.Chat.get_chat_data(M.chat_id)
        mute_list = chat_data.get("moderation", {}).get("mute_list", [])
        if user_id not in mute_list:
            mute_list.append(user_id)
            self.client.db.Chat.update_chat_datas(
                M.chat_id, {"moderation": {"mute_list": mute_list}}
            )
            await self.client.send_message(
                M.chat_id,
                f"🔇 Successfully **muted** @{user_name} in **{M.chat_title}**."
            )
        else:
            await self.client.send_message(
                M.chat_id,
                f"@{user_name} is already muted in **{M.chat_title}**."
            )

        await self.client.restrict_chat_member(M.chat_id, user_id, mute_permissions)
