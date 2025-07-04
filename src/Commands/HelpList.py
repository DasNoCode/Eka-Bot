from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "help",
                "category": "core",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": False,
                "ChatOnly": False,
                "description": {"content": "List all commands and their descriptions."},
            },
        )

    async def exec(self, M: Message, context):
        help_lines = []
        for cmd_name, cmd_obj in self.handler.commandMap.items():
            if cmd_obj.config.command == cmd_name:
                desc = getattr(getattr(cmd_obj.config, "description", {}), "content", "No description.")
                help_lines.append(f"/{cmd_name} - {desc}")
        help_text = "**Available Commands**\n" + "\n".join(sorted(help_lines))
        await self.client.send_message(M.chat_id, help_text)