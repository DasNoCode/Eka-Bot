import random
from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "sendgif",
                "category": "general",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": True,
                "ChatOnly": False,
                "description": {
                    "content": "Send you gif of your wish",
                    "usage": "/sendgif — Send you gif of your wish"
                },
            },
        )

    async def exec(self, M: Message, context):
        combined_text = context[1]
        for word in ["/sendgif", f"@{M.sender.user_name}"]:
            combined_text = combined_text.replace(word, "")
        return await self.client.send_animation(M.chat_id, random.choice((self.client.utils.get_tenor_gif_urls(combined_text))))