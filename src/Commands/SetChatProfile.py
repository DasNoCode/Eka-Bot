import os

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "chatprofile",
                "category": "chat",
                "xp": True,
                "AdminOnly": True,
                "OwnerOnly": False,
                "ChatOnly" : True,
                "description": {"content": "Set the chat profile picture"},
            },
        )

    async def exec(self, M: Message, contex):

        if M.msg_type is "photo":
            await self.client.send_message(
                M.chat_id, f"@{M.sender.user_name} Media isn't a photo"
            )

        await self.client.download_media(
            M.file_id,
            file_name=f"Images/{M.file_id}.jpg",
        )
        await self.client.set_chat_photo(
            M.chat_id, photo=f"src/Images/{M.file_id}.jpg"
        )
        return os.remove(f"src/Images/{M.file_id}.jpg")
