from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message

class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "user_leaderboard",
                "category": "general",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": False,
                "ChatOnly" : False,
                "description": {"content": "Show user leaderboard based on XP"},
            },
        )

    async def exec(self, M: Message, context):

        all_users = self.client.db.User.get_all_users()
        if callable(getattr(all_users, "__await__", None)):
            all_users = await all_users
        all_users = [u for u in all_users if u.get("user_id") is not None]

        user_rank, top_10 = self.client.calculate_rank("USER", M.sender.user_id, all_users)

        leaderboard_lines = ["🏆 **User Leaderboard (by XP)**\n"]
        medals = ["🥇", "🥈", "🥉"]

        for idx, user in enumerate(top_10, start=1):
            user_id = user.get("user_id")
            if not user_id:
                user_name = "Unknown"
            else:
                try:
                    user_obj = await self.client.get_users(user_id)
                    if getattr(user_obj, "username", None):
                        user_name = f"@{user_obj.username}"
                    else:
                        user_name = user_obj.first_name or "Unknown"
                        if getattr(user_obj, "last_name", None):
                            user_name += f" {user_obj.last_name}"
                except Exception:
                    user_name = "Unknown"

            xp = user.get("xp", 0)
            medal = medals[idx-1] if idx <= 3 else f"{idx}."
            leaderboard_lines.append(f"{medal} {user_name} — {xp} **XP**")

        current_user = next((u for u in all_users if u.get("user_id") == M.sender.user_id), None)
        current_xp = current_user.get("xp", 0) if current_user else 0

        leaderboard_lines.append(f"\n**Your Rank:** #{user_rank} ({current_xp} **XP**)")
        leaderboard_msg = "\n".join(leaderboard_lines)

        await self.client.send_message(M.chat_id, leaderboard_msg)