from datetime import datetime
import psutil

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "stats",
                "category": "owner",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": True,
                "ChatOnly": False,
                "description": {
                    "content": "Display system/server resource usage details.",
                    "usage": "Use `/stats` to check server CPU, memory, uptime, and current time/date."
                },
            },
        )

    async def exec(self, M: Message, context):
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%Y-%m-%d")
        uptime = self.client.utils.uptime()

        await self.client.send_message(
            M.chat_id,
            f"💻 **Server Status**\n\n"
            f"📅 **Date:** {current_date}\n"
            f"⏰ **Time:** {current_time}\n"
            f"⏳ **Uptime:** {uptime}\n"
            f"🧠 **CPU Usage:** {cpu_percent}%\n"
            f"💾 **Memory Usage:** {memory_percent}%"
        )
