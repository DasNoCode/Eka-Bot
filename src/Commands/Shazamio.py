import os

from aiohttp_retry import ExponentialRetry
from shazamio import HTTPClient, Serialize, Shazam

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "shazamio",
                "category": "general",
                "xp": True,
                "AdminOnly": False,
                "OwnerOnly": False,
                "ChatOnly": False,
                "description": {
                    "content": "Identify the song from audio or voice message.",
                    "usage": "Reply to or send an audio/voice message and use `/shazamio` to identify the song."
                },
            },
        )

    async def exec(self, M: Message, context):
        shazam = Shazam(
            http_client=HTTPClient(
                retry_options=ExponentialRetry(
                    attempts=12,
                    max_timeout=204.8,
                    statuses={500, 502, 503, 504, 429}
                ),
            )
        )

        async def recognize(path: str):
            result = await shazam.recognize(path)
            return Serialize.full_track(result)

        file_type = str(M.msg_type).lower()
        downloads_path = "src/downloads"

        if file_type == "audio":
            file_path = f"{downloads_path}/{M.file_id}.mp3"
            await self.client.download_media(M.file_id, file_name=file_path)
            result = await recognize(file_path)

        elif file_type == "voice":
            file_path = f"{downloads_path}/{M.id}.ogg"
            await self.client.download_media(M.voice.file_id, file_name=file_path)
            result = await recognize(file_path)

        else:
            return await self.client.send_message(
                M.chat_id,
                f"@{M.sender.user_name} please reply to an **audio** or **voice message** to recognize the song."
            )

        try:
            song_title = result.track.title
            release_date = result.track.sections[0].metadata[2].text
            cover_image = result.track.sections[0].meta_pages[1].image

            await self.client.send_photo(
                M.chat_id,
                cover_image,
                f"**🎵 Song Name:** `{song_title}`\n**📅 Released:** {release_date}"
            )
        except Exception as e:
            await self.client.send_message(M.chat_id, "⚠️ Failed to fetch song info.")
            self.client.log.error(f"Shazamio error: {e}")

        os.remove(file_path)
