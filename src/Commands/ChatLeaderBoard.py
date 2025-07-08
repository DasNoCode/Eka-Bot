from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message

class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "chat_leaderboard",
                "category": "chat",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": False,
                "ChatOnly": True,
                "description": {
                    "content": "Displays the leaderboard of chats based on total XP.",
                    "usage": "/chat_leaderboard\n\nShows top 10 chats ranked by XP and your current chat's rank and XP."
                },
            },
        )

    async def exec(self, message: Message, context):
        chat_data_list = self.client.db.Chat.get_all_chat_datas()
        chat_rank, top_10_chats = self.client.calculate_rank("CHAT", message.chat_id, chat_data_list)

        leaderboard_lines = ["🏆 **Chat Leaderboard (by XP)**\n"]
        medals = ["🥇", "🥈", "🥉"]

        for idx, chat_entry in enumerate(top_10_chats, start=1):
            chat_info = await self.client.get_chat(chat_entry["chat_id"])
            xp = chat_entry.get("xp", 0)
            medal = medals[idx - 1] if idx <= 3 else f"{idx}."
            leaderboard_lines.append(f"{medal} {chat_info.title} — {xp} **XP**")

        leaderboard_text = "\n".join(leaderboard_lines)

        current_chat_data = next((c for c in chat_data_list if c.get("chat_id") == message.chat_id), {})
        current_chat_xp = current_chat_data.get("xp", 0)

        leaderboard_text += f"\n\n**Your Chat Rank:** #{chat_rank} ({current_chat_xp} **XP**)"

        await self.client.send_message(message.chat_id, leaderboard_text)
