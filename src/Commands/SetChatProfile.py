import os

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "set_chat_profile",
                "category": "chat",
                "xp": True,
                "AdminOnly": True,
                "OwnerOnly": False,
                "ChatOnly": True,
                "description": {
                    "content": "Set a new profile picture for the group.",
                    "usage": "Reply to a photo with `/set_chat_profile` to set it as the group's display picture.\n\nOnly admins can use this command."
                },
            },
        )

    async def exec(self, M: Message, context):
        if M.msg_type != "photo":
            return await self.client.send_message(
                M.chat_id, f"@{M.sender.user_name} please reply to a **photo** to set it as the group profile picture."
            )

        image_path = f"Images/{M.file_id}.jpg"
        saved_path = f"src/{image_path}"

        await self.client.download_media(M.file_id, file_name=image_path)
        await self.client.set_chat_photo(M.chat_id, photo=saved_path)
        os.remove(saved_path)
