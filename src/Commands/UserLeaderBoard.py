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
                "ChatOnly": False,
                "description": {
                    "content": "Displays a leaderboard sorted by user XP.",
                    "usage": "`/user_leaderboard` to view the top XP holders and your rank."
                },
            },
        )

    async def exec(self, M: Message, context):

        all_users = self.client.db.User.get_all_users()
        if callable(getattr(all_users, "__await__", None)):
            all_users = await all_users

        users_with_ids = [user for user in all_users if user.get("user_id") is not None]

        user_rank, top_users = self.client.calculate_rank("USER", M.sender.user_id, users_with_ids)

        leaderboard_lines = ["🏆 **User Leaderboard (by XP)**\n"]
        medals = ["🥇", "🥈", "🥉"]

        for index, user_data in enumerate(top_users, start=1):
            user_id = user_data.get("user_id")
            user_xp = user_data.get("xp", 0)

            if user_id:
                try:
                    tg_user = await self.client.get_users(user_id)
                    if tg_user.username:
                        display_name = f"@{tg_user.username}"
                    else:
                        display_name = tg_user.first_name or "Unknown"
                        if tg_user.last_name:
                            display_name += f" {tg_user.last_name}"
                except Exception:
                    display_name = "Unknown"
            else:
                display_name = "Unknown"

            prefix = medals[index - 1] if index <= 3 else f"{index}."
            leaderboard_lines.append(f"{prefix} {display_name} — {user_xp} **XP**")

        current_user_data = next((u for u in users_with_ids if u.get("user_id") == M.sender.user_id), None)
        current_user_xp = current_user_data.get("xp", 0) if current_user_data else 0

        leaderboard_lines.append(f"\n**Your Rank:** #{user_rank} ({current_user_xp} **XP**)")
        leaderboard_text = "\n".join(leaderboard_lines)

        await self.client.send_message(M.chat_id, leaderboard_text)
