from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "repot",
                "category": "general",
                "xp": True,
                "AdminOnly": False,
                "OwnerOnly": False,
                "ChatOnly": False,
                "description": {
                    "content": "repot the bug to owner directly",
                    "usage": "/repot — repot the bug to owner directly"
                },
            },
        )

    async def exec(self, M: Message, context):
        if M.msg_type in ["voice", "animation", "audio", "photo", "video"]:
            return
        if M.reply_to_message:
            combined_text = M.reply_to_message.text
        else:
            combined_text = context[1]
        await self.client.send_message(self.client.owner_id, combined_text+f"\nRepot from @{M.sender.user_name}")
        await self.client.send_message(M.chat_id, f"@{M.sender.user_name}Sucessfully informed the owner!")