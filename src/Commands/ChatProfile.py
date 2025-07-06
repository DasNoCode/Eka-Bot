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
                "ChatOnly" : True,
                "description": {"content": "Show the profile and stats of this chat."},
            }
        )

    async def exec(self, M: Message, context):
        chatTitle = M.chat_title
        chatId = M.chat_id
        
        profilePhotoId = getattr(M.chat_info.photo, "big_file_id", None)
        imageFileName = f"Images/{chatId}.jpg"
        photoPath = None
        
        if profilePhotoId:
            await self.client.download_media(
                profilePhotoId,
                file_name=imageFileName
            )
            photoPath = f"src/{imageFileName}"

        chatData = self.client.db.Chat.get_chat_data(chatId)
        if not chatData:
            await self.client.send_message(chatId, "No data found for this chat.")
            return
        
        settings = chatData.get("settings", {})
        stats = chatData.get("stats", {})
        moderation = chatData.get("moderation", {})
        
        statusMessage = (
            "🏠 **Chat Profile**\n\n"
            f"📝 **Title:** {chatTitle}\n"
            f"🆔 **Chat ID:** `{chatId}`\n"
            f"🎖️ **Level:** {chatData.get('lvl', 0)}\n"
            f"📈 **XP:** {chatData.get('xp', 0)}\n"
            f"🤖 **Bot Admin:** {'✅' if chatData.get('is_bot_admin') else '❌'}\n\n"
            
            f"⚙️ **Settings**\n"
            f"• 🌐 **Language:** {settings.get('language', 'en')}\n"
            f"• 🎉 **Events:** {'✅' if settings.get('events') else '❌'}\n"
            f"• 🔐 **Captchas:** {'✅' if settings.get('captchas') else '❌'}\n"
            f"• 👋 **Welcome:** {'✅' if settings.get('welcome_enabled') else '❌'}\n"
            f"• 💬 **Welcome Msg:** {settings.get('welcome_message', 'Not set')}\n\n"
        
            f"📊 **Stats**\n"
            f"• 📨 **Messages:** {stats.get('messages_count', 0)}\n"
            f"• 👥 **Active Users:** {len(stats.get('active_users', []))}\n\n"
        
            f"🛡️ **Moderation**\n"
            f"• 🚫 **Banned Users:** {len(moderation.get('banned_users', []))}\n"
            f"• 🔇 **Muted Users:** {len(moderation.get('mute_list', []))}\n"
            f"• 📢 **Broadcast:** {'✅' if chatData.get('BrodCast') else '❌'}"
        )
        
        if photoPath:
            await self.client.send_photo(
                chatId,
                photo=photoPath,
                caption=statusMessage
            )
            os.remove(photoPath)
        else:
            await self.client.send_message(chatId, statusMessage)
        