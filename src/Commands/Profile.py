import os
from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "profile",
                "category": "general",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": False,
                "ChatOnly": False,
                "description": {
                    "content": "View a user's profile and stats.",
                    "usage": "/profile [mention or reply] — Shows the user's detailed profile."
                },
            }
        )
    
    async def exec(self, M: Message, context):
        if M.reply_to_message and getattr(M.reply_to_message, 'replied_user', None):
            user = M.reply_to_message.replied_user
        elif M.mentioned:
            user = M.mentioned[0]
        else:
            user = M.sender
        
        profile_id = user.user_profile_id
        user_id = user.user_id
        user_name = user.user_name
        
        file_path = f'Images/{user_id}.jpg'
        
        await self.client.download_media(
            profile_id,
            file_name=file_path
        )
        
        user_data = self.client.db.User.get_user(user_id)
        
        status = (
            "👤 **𝗨𝘀𝗲𝗿 𝗣𝗿𝗼𝗳𝗶𝗹𝗲**\n\n"
            f"✨ **Username:** @{user_name}\n"
            f"🆔 **ID:** {user_data.get('user_id')}\n"
            f"🎖️ **Level:** {user_data.get('lvl')}\n"
            f"📈 **XP:** {user_data.get('xp')}\n"
            f"🏅 **Rank:** #{user_data.get('rank')}\n\n"
        )

        afk = user_data.get('afk', {})
        if afk.get('is_afk'):
            status += (
                f"💤 **AFK:** AFK 🟡\n"
                f"   • **Reason:** {afk.get('afk_reason', 'No reason')}\n"
                f"   • **Since:** {afk.get('time', 'Unknown')} UTC\n\n"
            )
        else:
            status += "**💤 AFK:** Not AFK 🟢\n\n"
        
        tic = user_data.get('tic_tac_toe', {})
        rps = user_data.get('rps', {})
        status += (
            "🎮 **Games**\n"
            f"• 🟦 **Tic Tac Toe:** {tic.get('win', 0)} **|** {tic.get('total_game_played', 0)} **Played**\n"
            f"• ✊ **Rock Paper Scissors:** {rps.get('win', 0)} **|** {rps.get('total_game_played', 0)} **Played**\n\n"
        )
        

        ban = user_data.get('ban', {})
        if ban.get('is_ban'):
            status += (
                "🚫 **Ban Status:** Banned\n"
                f"   • **Reason:** {ban.get('reason', 'No reason')}\n"
                f"   • **Since:** {ban.get('time', 'Unknown')} UTC\n"
                f"   • **Total Bans:** {ban.get('no_of', 1)}"
            )
        else:
            status += "🚫 **Ban Status:** Not Banned"
        
        await self.client.send_photo(
            M.chat_id,
            photo=f"src/{file_path}",
            caption=status
        )
        
        os.remove(f"src/{file_path}")
