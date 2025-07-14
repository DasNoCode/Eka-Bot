from datetime import datetime

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "afk",
                "category": "chat",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": False,
                "ChatOnly": True,
                "description": {
                    "content": "Mark yourself as AFK (Away From Keyboard). Other users will be notified when they mention you.",
                    "usage": "/afk [reason]\n\nExamples:\n/afk\n/afk Out for lunch"
                },
            },
        )

    async def exec(self, M: Message, context):
        current_time_str = datetime.now().strftime("%H:%M:%S")
        sender_id = M.sender.user_id
        sender_username = M.sender.user_name
    
        user_data = self.client.db.User.get_user(sender_id)
    
        if context[2].get("type") == "afk_btn":
            afk_user_id = int(context[2].get("user_id"))
            afk_user_data = self.client.db.User.get_user(afk_user_id)
    
            tagged_messages = afk_user_data.get("afk", {}).get("tagged_msgs", [])
            afk_start_time_str = afk_user_data.get("afk", {}).get("time")
    
            if not afk_start_time_str:
                return await self.client.send_message(M.chat_id, "AFK time not found.")
    
            afk_start_time = datetime.strptime(afk_start_time_str, "%H:%M:%S")
            current_time = datetime.strptime(current_time_str, "%H:%M:%S")
            afk_duration = str(current_time - afk_start_time)
    
            response_text = (
                f"Welcome back @{sender_username}! You were AFK for {afk_duration}.\n"
                f"Here are the messages you were tagged in:\n\n"
            )
    
            for index, msg in enumerate(tagged_messages, start=1):
                chat_id = str(msg.get("chat_id")).removeprefix("-100")
                msg_id = msg.get("message_id")
                response_text += f"{index}. https://t.me/c/{chat_id}/{msg_id}\n"
    
            self.client.db.User.set_afk(sender_id, False, None, current_time_str)
            self.client.db.User.update_user(afk_user_id, {"afk": {"tagged_msgs": []}})
    
            await self.client.send_message(M.chat_id, response_text)
            return
    
        if user_data.get("afk", {}).get("is_afk"):
            return await self.client.send_message(
                M.chat_id, f"@{sender_username}, you are already marked as AFK."
            )
    
        afk_reason = context[1] or None
        self.client.db.User.set_afk(sender_id, True, afk_reason, current_time_str)
    
        await self.client.send_message(
            M.chat_id, f"@{sender_username} is now marked as AFK!"
        )
    