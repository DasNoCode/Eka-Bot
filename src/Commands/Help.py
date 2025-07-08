from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "help",
                "category": "general",
                "xp": True,
                "AdminOnly": False,
                "OwnerOnly": False,
                "ChatOnly": False,
                "description": {
                    "content": "Get info about the command.",
                    "usage": "/help or /help <command>"
                },
            },
        )

    async def exec(self, M: Message, context):
        if not context[3]:
            return await self.client.send_message(M.chat_id, "/help Get info about the command.")
        for cmd_name, cmd_obj in self.handler.commandMap.items():
            if cmd_name == context[3][0]:
                return await self.client.send_message(M.chat_id, f"**command name**: {cmd_name}\n**description:** {cmd_obj.config.description.content}\n**usage:** {cmd_obj.config.description.usage}")
        else:
            return await self.client.send_message(M.chat_id, "command not found!")