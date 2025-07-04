from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup

from Structures.Client import SuperClient

CHAT_IDS = {}


class EventHandler:

    def __init__(self, client: SuperClient):
        self.__client = client

    async def handler(self, message):
        chat_data = self.__client.db.Chat.get_chat_data(message.chat.id)
        if str(message.service).split(".")[-1] == "NEW_CHAT_MEMBERS":
            members = message.new_chat_members
            for member in members:
                self.member = member
            
            if chat_data.get("settings").get("captchas"):
                await self.__client.restrict_chat_member(
                    message.chat.id,
                    self.member.id,
                    ChatPermissions(can_send_messages=False),
                )
                keybord = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Captcha",
                                callback_data=f"/captcha --type=btn --user_id={self.member.id}",
                            )
                        ]
                    ]
                )
                msg = await self.__client.send_message(
                    message.chat.id,
                    f"__@{self.member.username} has joined the Chat !\nSolve the captcha__",
                    reply_markup=keybord,
                )

                CHAT_IDS[self.member.id] = msg.id


        if not chat_data.get("settings").get("events"):
            return
        if str(message.service).split(".")[-1] == "NEW_CHAT_MEMBERS":
            await self.__client.send_message(
                message.chat.id,
                f"__@{self.member.username} has joined the Chat !__",
            )
        elif str(message.service).split(".")[-1] == "LEFT_CHAT_MEMBERS":
            await self.__client.send_message(
                message.chat.id,
                f"__@{message.left_chat_member.username} has left the Chat.__",
            )
        elif str(message.service).split(".")[-1] == "PINNED_MESSAGE":
            await self.__client.send_message(message.chat.id, f"__A new message has been pinned by @{message.from_user.username}./nCheck now !__",)
