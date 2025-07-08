import os
import tracemoepy

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    media_types = {"photo": "jpg", "video": "mp4", "animation": "gif"}

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "whatanime",
                "category": "general",
                "xp": True,
                "AdminOnly": False,
                "OwnerOnly": False,
                "ChatOnly": False,
                "description": {
                    "content": "Identify the anime from an image, GIF, or video clip.",
                    "usage": "Reply to a photo, gif, or video with `/whatanime` to search for the anime scene."
                },
            },
        )
        self.tracemoe = tracemoepy.tracemoe.TraceMoe()

    async def exec(self, message: Message, context):
        msg_type = message.msg_type
        sender_name = message.sender.user_name

        if msg_type not in self.media_types:
            return await self.client.send_message(
                message.chat_id,
                f"@{sender_name}, please reply to a **photo**, **gif**, or **video** to identify the anime.",
            )

        file_ext = self.media_types[msg_type]
        file_path = f"Images/{message.file_id}.{file_ext}"
        full_path = f"src/{file_path}"

        await self.client.download_media(message.file_id, file_name=file_path)

        try:
            result = self.tracemoe.search(full_path, upload_file=True)

            if isinstance(result.result, list) and result.result:
                top_result = result.result[0]
                anilist = top_result.get("anilist", {})
                titles = anilist.get("title", {})
                native_title = titles.get("native", "N/A")
                english_title = titles.get("english", "N/A")
                is_adult = anilist.get("isAdult", "N/A")
                episode = top_result.get("episode", "N/A")
                similarity = top_result.get("similarity", 0.0)

                await self.client.send_message(
                    message.chat_id,
                    f"🎬  **Anime Identified**\n\n"
                    f"**Native Title:** `{native_title}`\n"
                    f"**English Title:** `{english_title}`\n"
                    f"**Episode:** `{episode}`\n"
                    f"**Adult Content:** {'Yes 🔞' if is_adult else 'No'}\n"
                    f"**Similarity:** `{similarity * 100:.2f}%`"
                )
            else:
                await self.client.send_message(message.chat_id, "❌ No matching anime found.")
        except Exception as e:
            self.client.log.error(f"TraceMoe error: {e}")
            await self.client.send_message(message.chat_id, "⚠️ Something went wrong while identifying the anime.")
        finally:
            if os.path.exists(full_path):
                os.remove(full_path)
