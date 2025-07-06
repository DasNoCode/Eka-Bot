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
                "ChatOnly" : True,
                "description": {"content": "Show chat leaderboard based on XP"},
            },
        )

    async def exec(self, M: Message, context):
        chat_data_list = self.client.db.Chat.get_all_chat_datas()
        chat_rank, top_10 = self.client.calculate_rank("CHAT", M.chat_id, chat_data_list)
        leaderboard_lines = ["🏆 **Chat Leaderboard (by XP)**\n"]
        medals = ["🥇", "🥈", "🥉"]
        for idx, chat in enumerate(top_10, start=1):
            title = await self.client.get_chat(chat["chat_id"])
            xp = chat.get("xp")
            medal = medals[idx-1] if idx <= 3 else f"{idx}."
            leaderboard_lines.append(f"{medal} {title.title} — {xp} **XP**")
        
        leaderboard_msg = "\n".join(leaderboard_lines)

        current_chat = next((c for c in chat_data_list if c.get("chat_id") == M.chat_id), None)
        current_xp = current_chat.get("xp")
        leaderboard_msg += f"\n\n**Your Chat Rank:** #{chat_rank} ({current_xp} **XP**)"

        await self.client.send_message(M.chat_id, leaderboard_msg)