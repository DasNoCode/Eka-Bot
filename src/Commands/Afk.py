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
        current_time = datetime.now().time().strftime("%H:%M:%S")
        user_data = self.client.db.User.get_user(M.sender.user_id)
        
        if context[2].get("type") == "afk_btn":
            print(context[2].get("user_id"))
            userData = self.client.db.User.get_user(context[2].get("user_id"))
            msg_ids = userData.get("afk", {}).get("tagged_msgs", [])
            print(msg_ids)
        
            text = f"Welcome back! @{M.sender.user_name}\nHere are the messages you were tagged in:\n\n"
            for index, (msg_id, chat_id) in enumerate(msg_ids, start=1):
                cleaned_chat_id = str(chat_id).removeprefix("-100")
                print(cleaned_chat_id, msg_id)
                text += f"{index}. Message ID: {msg_id}, Chat ID: {cleaned_chat_id}\n"
        
            await self.client.send_message(M.chat_id, text)
            return  
        
        if user_data.get("afk", {}).get("is_afk"):
            return await self.client.send_message(
                M.chat_id, f"@{M.sender.user_name}, you are already marked as AFK."
            )
        
        afk_reason = context[1] if context[1] else None
        self.client.db.User.set_afk(M.sender.user_id, True, afk_reason, current_time)
        
        await self.client.send_message(
            M.chat_id, f"@{M.sender.user_name} is now marked as AFK!"
        )
