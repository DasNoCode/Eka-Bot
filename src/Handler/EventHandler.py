from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup
from Structures.Client import SuperClient



class EventHandler:

    msg_id = 0

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
                                callback_data=f"/captcha --type=captcha_btn --user_id={self.member.id}",
                            )
                        ]
                    ]
                )
                msg = await self.__client.send_message(
                    message.chat.id,
                    f"__@{self.member.username} Thank for joining!\nTo proof you are human slove this **captcha**!__",
                    reply_markup=keybord,
                )
                EventHandler.msg_id = msg.id
                


        if not chat_data.get("settings").get("events"):
            return
        if str(message.service).split(".")[-1] == "NEW_CHAT_MEMBERS":
            if not chat_data.get("settings").get("captchas"):
                await self.__client.send_message(
                    message.chat.id,
                    f"@{self.member.username} has joined the Chat!",
                )
        elif str(message.service).split(".")[-1] == "LEFT_CHAT_MEMBERS":
            await self.__client.send_message(
                message.chat.id,
                f"@{message.left_chat_member.username} has left the Chat!",
            )
        elif str(message.service).split(".")[-1] == "PINNED_MESSAGE":
            await self.__client.send_message(message.chat.id, f"A new message has been pinned by @{message.from_user.username}./nCheck now !",)
