from pyigdl import IGDownloader

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "igdl",
                "category": "downloader",
                "xp": True,
                "AdminOnly": False,
                "OwnerOnly": False,
                "ChatOnly" : False,
                "description": {"content": "Download the Instagram reels and photo."},
            },
        )

    async def exec(self, M: Message, contex):
        if M.reply_to_message:
            try:
                url = self.client.utils.get_urls(M.reply_to_message.text)
                data = IGDownloader(url)
                return await self.client.send_video(M.chat_id, data[0]["download_link"])
            except Exception as e:
                return await self.client.send_message(
                    M.chat_id, "Provide a IG video link🔗 to download."
                )
        if not len(M.urls):
            return await self.client.send_message(
                M.chat_id, "Provide a IG video link🔗 to download."
            )

        data = IGDownloader(M.urls[0])
        return await self.client.send_video(M.chat_id, data[0]["download_link"])
