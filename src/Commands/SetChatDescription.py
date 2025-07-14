from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "set_chat_description",
                "category": "chat",
                "xp": False,
                "AdminOnly": True,
                "OwnerOnly": False,
                "ChatOnly": True,
                "description": {
                    "content": "set it as chat description",
                    "usage": "/set_chat_description — replied to to text it will set it as chat description"
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
        for word in ["/set_chat_description", f"@{M.sender.user_name}"]:
            combined_text = combined_text.replace(word, "")
        await self.client.set_chat_description(M.chat_id, combined_text)