import asyncio
import os
import random
import string

from captcha.image import ImageCaptcha
from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup

from Handler.EventHandler import EventHandler
from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "captcha",
                "category": "chat",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": False,
                "ChatOnly": True,
                "description": {
                    "content": "Prevents bots from joining"
                },
            }
        )
        self.generatedCaptchaCode = None
        self.captchaMessageId = None

    async def exec(self, message: Message, context):

        previousMessageId = EventHandler.msg_id

        if not message.is_callback:
            return

        userIdFromContext = int(context[2].get("user_id"))

        if userIdFromContext != message.sender.user_id and not message.isAdmin:
            return

        if context[2].get("code"):
            if context[2].get("code") == self.generatedCaptchaCode:
                await self.client.restrict_chat_member(
                    message.chat_id,
                    userIdFromContext,
                    ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True
                    ),
                )

                await self.client.delete_messages(
                    message.chat_id,
                    self.captchaMessageId
                )

                await self.client.send_message(
                    message.chat_id,
                    f"@{message.sender.user_name}, Enjoy your stay here! And use /help to get all the bot commands"
                )
            else:
                await self.client.ban_chat_member(
                    message.chat_id,
                    userIdFromContext
                )

            await self.client.delete_messages(
                message.chat_id,
                previousMessageId
            )
            return

        generateRandomCode = lambda: "".join(
            random.choices(string.ascii_letters + string.digits, k=5)
        )

        captchaCodeOptions = {
            f"code{i}": generateRandomCode() for i in range(1, 4)
        }

        self.generatedCaptchaCode = random.choice(list(captchaCodeOptions.values()))

        captchaImage = ImageCaptcha(fonts=["src/CaptchaFonts/Roboto-Thin.ttf"])
        imagePath = f"src/Images/{userIdFromContext}.png"
        captchaImage.write(self.generatedCaptchaCode, imagePath)

        await self.client.delete_messages(
            message.chat_id,
            previousMessageId
        )

        captchaPromptMessage = await self.client.send_photo(
            message.chat_id,
            imagePath,
            caption="Here is your **Captcha**! Solve it within 1 minute.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=code,
                            callback_data=f"/captcha --code={code} --user_id={userIdFromContext}"
                        )
                    ]
                    for code in captchaCodeOptions.values()
                ]
            ),
        )

        self.captchaMessageId = captchaPromptMessage.id

        asyncio.create_task(self.startCaptchaTimer(message.chat_id))

        os.remove(imagePath)

    async def startCaptchaTimer(self, chatId):
        try:
            await asyncio.sleep(60)
            await self.client.delete_messages(
                chat_id=chatId,
                message_ids=self.captchaMessageId
            )
        except Exception:
            pass
