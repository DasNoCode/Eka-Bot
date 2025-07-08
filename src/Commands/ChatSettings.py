from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message

class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "set",
                "category": "chat",
                "xp": False,
                "AdminOnly": True,
                "OwnerOnly": False,
                "ChatOnly": True,
                "description": {
                    "content": "Modify chat settings like captcha, welcome messages, and events.",
                    "usage": "/set — Opens interactive settings\n/set --type=captcha — Toggle captcha\n/set --type=welcome_enabled — Toggle welcome\n/set --type=welcome_message — Reply to a message to set as welcome message"
                },
            },
        )

    async def exec(self, message: Message, context):
        chat_id = message.chat_id
        chat_title = message.chat_title
        sender_name = message.sender.user_name

        chat_data = self.client.db.Chat.get_chat_data(chat_id)
        settings = chat_data.get("settings", {})

        if not context[2]:
            markup = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        f"Captcha {' 🔹' if settings.get('captchas') else ' 🔺'}",
                        callback_data="/set --type=captchas --data=True",
                    )
                ],
                [
                    InlineKeyboardButton(
                        f"Event {' 🔹' if settings.get('events') else ' 🔺'}",
                        callback_data="/set --type=events --data=True",
                    )
                ],
                [
                    InlineKeyboardButton(
                        f"Welcome Enabled {' 🔹' if settings.get('welcome_enabled') else ' 🔺'}",
                        callback_data="/set --type=welcome_enabled --data=True",
                    )
                ],
            ])
            self.btn_msg = await self.client.send_message(chat_id, "**Chat Settings:**", reply_markup=markup)
            return

        setting_type = context[2].get("type")


        if setting_type == "welcome_message":
            if not message.reply_to_message:
                return await self.client.send_message(
                    chat_id, f"@{sender_name}, please reply to the message you want to set as welcome!"
                )

            self.client.db.Chat.update_chat_datas(chat_id, {
                "settings": {
                    "events": True,
                    "welcome_message": message.reply_to_message.text
                }
            })
            return await self.client.send_message(
                chat_id,
                f"**Welcome msg** set to:\n\n`{message.reply_to_message.text}`\n\nIn **{chat_title}**",
            )

        elif setting_type in ["captchas", "events", "welcome_enabled"]:
            current_value = settings.get(setting_type, False)
            new_value = not current_value

            self.client.db.Chat.update_chat_datas(chat_id, {"settings": {setting_type: new_value}})

            setting_label = setting_type.replace("_", " ").title()
            status = "activated 🔹" if new_value else "deactivated 🔺"

            response = f"**{setting_label}** is {status} in:\n\n**{chat_title}**"

            if setting_type == "welcome_enabled" and new_value:
                response += (
                    "\n\nTo set a custom welcome message, reply to any message with:\n"
                    "`/set --type=welcome_message`"
                )
            elif setting_type == "events" and not new_value:
                response += (
                    "\n\n(Note: Welcome messages are now disabled, but can be re-enabled manually.)"
                )

            await self.client.send_message(chat_id, response)

        if hasattr(self, "btn_msg"):
            await self.client.delete_messages(chat_id=chat_id, message_ids=self.btn_msg.id)
