from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "banlist",
                "category": "chat",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": False,
                "ChatOnly": True,
                "description": {
                    "content": "Display a list of users who are currently banned from using the bot.",
                    "usage": "/banlist\n\nShows a list of all users banned from using the bot, along with their ban reasons."
                },
            },
        )

    async def exec(self, message: Message, context):
        all_users = self.client.db.User.get_all_users()
        banned_users = []

        for user in all_users:
            ban_data = user.get("ban", {})
            if ban_data.get("is_ban"):
                user_id = user.get("user_id")
                reason = ban_data.get("reason", "No reason provided")
                banned_users.append(f"**User ID:** {user_id}\n**Reason:** {reason}")

        if not banned_users:
            response_text = "✅ No users are currently **banned**."
        else:
            response_text = f"🚫 **Total Banned Users:** {len(banned_users)}\n\n" + "\n\n".join(banned_users)

        await self.client.send_message(message.chat_id, response_text)
