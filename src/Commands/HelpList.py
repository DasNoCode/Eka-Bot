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
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": False,
                "ChatOnly": False,
                "description": {"content": "List all commands and their descriptions."},
            },
        )

    async def exec(self, M: Message, context):
        general_cmds = []
        group_cmds = []
        game_cmds = []
        downloader_cmds = []

        for cmd_name, cmd_obj in self.handler.commandMap.items():
            category = cmd_obj.config.category
            if category == "general":
                general_cmds.append(f"{cmd_name}")
            elif category == "chat":
                group_cmds.append(f"{cmd_name}")
            elif category == "game":
                game_cmds.append(f"{cmd_name}")
            elif category == "downloader":
                downloader_cmds.append(f"{cmd_name}")

        format_cmds = lambda cmds: ",  ".join(f"__•{cmd}__" for cmd in sorted(cmds))

        help_text = (
            "\n"
            "🤖 **GENERAL COMMANDS**\n"
            f"{format_cmds(general_cmds)}\n\n"
            "👥 **GROUP / CHAT COMMANDS**\n"
            f"{format_cmds(group_cmds)}\n\n"
            "🎮 **GAME COMMANDS**\n"
            f"{format_cmds(game_cmds)}\n\n"
            "📂 **DOWNLOADER COMMANDS**\n"
            f"{format_cmds(downloader_cmds)}\n\n"
            "🙌 **SUPPORT ME**\n"
            "⭐️ **GitHub:** DasNoCode\n"
            "📸 **Instagram:** das_abae "
            
        )

        await self.client.send_message(M.chat_id, help_text)
