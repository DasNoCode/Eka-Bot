import os
from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "sticker",
                "category": "general",
                "xp": True,
                "AdminOnly": False,
                "OwnerOnly": False,
                "ChatOnly": False,
                "description": {
                    "content": "Convert an image or gif to a Telegram sticker.",
                    "usage": "`/sticker` — Reply to an image, animation, or gif to convert it into a sticker."
                }}
        )

    async def exec(self, M: Message, context):
        allowed_types = ["photo", "animation", "gif"]
        if M.msg_type not in allowed_types:
            await self.client.send_message(M.chat_id, "Only photo, animation, or gif files are supported.")
            return

        ext = "jpg" if M.msg_type == "photo" else "gif"
        file_base = f"{M.file_id}"
        download_path = f"Images/{file_base}.{ext}"
        await self.client.download_media(M.file_id, file_name=download_path)
        self.client.utils.convert_to_webp(f"src/{download_path}")
        await self.client.send_sticker(chat_id=M.chat_id, sticker=f"src/Images/{file_base}.webp")

        os.remove(f"src/{download_path}")
        os.remove(f"src/Images/{file_base}.webp")

