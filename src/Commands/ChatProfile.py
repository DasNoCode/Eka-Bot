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
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": False,
                "ChatOnly": True,
                "description": {
                    "content": "Displays the full profile and stats of the current chat.",
                    "usage": "/chatprofile\n\nShows chat title, XP, bot status, settings, message stats, and moderation data."
                }
            }
        )

    async def exec(self, message: Message, context):
        chat_title = message.chat_title
        chat_id = message.chat_id

        profile_photo_id = getattr(message.chat_info.photo, "big_file_id", None)
        local_image_path = f"Images/{chat_id}.jpg"
        full_image_path = None

        if profile_photo_id:
            await self.client.download_media(profile_photo_id, file_name=local_image_path)
            full_image_path = f"src/{local_image_path}"

        chat_data = self.client.db.Chat.get_chat_data(chat_id)
        if not chat_data:
            return await self.client.send_message(chat_id, "❌ No data found for this chat.")

        settings = chat_data.get("settings", {})
        stats = chat_data.get("stats", {})
        moderation = chat_data.get("moderation", {})

        profile_text = (
            "🏠 **Chat Profile**\n\n"
            f"📝 **Title:** {chat_title}\n"
            f"🆔 **Chat ID:** `{chat_id}`\n"
            f"🎖️ **Level:** {chat_data.get('lvl', 0)}\n"
            f"📈 **XP:** {chat_data.get('xp', 0)}\n"
            f"🤖 **Bot Admin:** {'✅' if chat_data.get('is_bot_admin') else '❌'}\n\n"

            f"⚙️ **Settings**\n"
            f"• 🌐 **Language:** {settings.get('language', 'en')}\n"
            f"• 🎉 **Events:** {'✅' if settings.get('events') else '❌'}\n"
            f"• 🔐 **Captchas:** {'✅' if settings.get('captchas') else '❌'}\n"
            f"• 👋 **Welcome:** {'✅' if settings.get('welcome_enabled') else '❌'}\n"
            f"• 💬 **Welcome Msg:** {settings.get('welcome_message', 'Not set')}\n\n"

            f"📊 **Stats**\n"
            f"• 📨 **Messages:** {stats.get('messages_count', 0)}\n"
            f"• 👥 **Active Users:** {len(stats.get('active_users', []) or [])}\n\n"

            f"🛡️ **Moderation**\n"
            f"• 🚫 **Banned Users:** {len(moderation.get('banned_users', []) or [])}\n"
            f"• 🔇 **Muted Users:** {len(moderation.get('mute_list', []) or [])}\n"
            f"• 📢 **Broadcast:** {'✅' if chat_data.get('BrodCast') else '❌'}"
        )

        if full_image_path:
            await self.client.send_photo(chat_id, photo=full_image_path, caption=profile_text)
            os.remove(full_image_path)
        else:
            await self.client.send_message(chat_id, profile_text)
