from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message

class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "mutedlist",
                "category": "chat",
                "xp": False,
                "AdminOnly": True,
                "OwnerOnly": False,
                "ChatOnly" : True,
                "description": {"content": "List all muted users in the chat"},
            },
        )

    async def exec(self, M: Message, contex):
        chat_data = self.client.db.Chat.get_chat_data(M.chat_id)
        mute_list = chat_data.get("moderation", {}).get("mute_list", [])

        if not mute_list:
            return await self.client.send_message(M.chat_id, "No users are currently muted in this chat.")

        muted_users_info = []
        for user_id in mute_list:
            try:
                user = await self.client.get_users(user_id)
                user_display = f"@{user.username}" if user.username else f"{user.first_name or ''} {user.last_name or ''}".strip()
                muted_users_info.append(f"- {user_display} (`{user_id}`)")
            except Exception:
                muted_users_info.append(f"- [Unknown User] (`{user_id}`)")

        await self.client.send_message(M.chat_id, "**Muted users in this chat:**\n" + "\n".join(muted_users_info))