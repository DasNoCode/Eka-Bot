from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message
import re


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "ban",
                "category": "owner",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": True,
                "ChatOnly": False,
                "description": {
                    "content": "Ban a user from using the bot. Can be used with an optional reason and ban duration.",
                    "usage": "/ban @username [reason] [time=duration]\n\nExamples:\n/ban @toxic_user Being annoying time=3days\nReply to a user's message with /ban to ban them directly."
                },
            },
        )

    async def exec(self, message: Message, context):
        if message.reply_to_message:
            target_username = message.reply_to_message.replied_user.user_name
            target_user_id = message.reply_to_message.replied_user.user_id
        elif message.mentioned:
            mentioned_user = message.mentioned[0]
            target_username = mentioned_user.user_name
            target_user_id = mentioned_user.user_id
        else:
            return await self.client.send_message(
                message.chat_id, f"@{message.sender.user_name}, please mention or reply to a user to ban them!"
            )

        if target_user_id == self.client.bot_id:
            return await self.client.send_message(
                message.chat_id, f"@{message.sender.user_name}, you can't ban me!"
            )

        ban_data = self.client.db.User.get_user(user_id=target_user_id).get("ban")
        if ban_data.get("is_ban"):
            return await self.client.send_message(
                message.chat_id, f"@{message.sender.user_name}, this user is already **banned!**"
            )

        if context[2]:
            reason_text = context[2].get("reason", "") or ""
            raw_time_text = context[2].get("time", "")
            combined_text = f"{reason_text} {raw_time_text}"
        else:
            combined_text = context[1]
            for word in ["/ban", f"@{target_username}"]:
                combined_text = combined_text.replace(word, "")
        
        time_pattern = re.compile(
            r"(?:time\s*=\s*)?(?P<num>\d+)?\s*(?P<unit>seconds?|minutes?|hours?|days?|weeks?|months?|years?)\b",
            re.IGNORECASE,
        )
        seconds_map = {
            "second": 1,
            "minute": 60,
            "hour": 3600,
            "day": 86400,
            "week": 604800,
            "month": 2592000,
            "year": 31536000,
        }

        ban_duration = None
        match = time_pattern.search(combined_text)
        if match:
            num = int(match.group("num")) if match.group("num") else 1
            unit = match.group("unit").rstrip("s").lower()
            ban_duration = num * seconds_map[unit]
            combined_text = time_pattern.sub("", combined_text)

        reason_cleaned = re.sub(r"\btime\b", "", combined_text, flags=re.IGNORECASE)
        reason_cleaned = " ".join(reason_cleaned.split())

        self.client.db.User.update_user(
            target_user_id,
            {
                "ban": {
                    "no_of": ban_data.get("no_of", 0) + 1,
                    "is_ban": True,
                    "reason": reason_cleaned,
                    "time": ban_duration,
                }
            },
        )

        updated_ban_data = self.client.db.User.get_user(user_id=target_user_id).get("ban")
        ban_status = "\n".join([
            "🚫 **Ban Status:** Banned",
            f"   **• Reason:** {updated_ban_data.get('reason', '')}",
            f"   **• Since:** {updated_ban_data['time']} UTC" if updated_ban_data.get("time") else "   **• Since:**",
            f"   **• Total Bans:** {updated_ban_data.get('no_of', 1)}",
        ])

        await self.client.send_message(
            message.chat_id,
            f"Successfully **banned** @{target_username} from using @{message.bot_username}\n\n{ban_status}",
        )
