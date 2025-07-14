from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "commands",
                "category": "general",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": False,
                "ChatOnly": False,
                "description": {
                    "content": "List all available commands by category.",
                    "usage": "/help or /help <command>"
                },
            },
        )

    async def exec(self, M: Message, context):
        category_commands = {}

        for cmd_name, cmd_obj in self.handler.commandMap.items():
            category = cmd_obj.config.category or "uncategorized"
            category = category.capitalize()
            if category not in category_commands:
                category_commands[category] = []
            category_commands[category].append(cmd_name)

        def format_cmds(cmds):
            return "**➛  **" + ", ".join(sorted(cmds))

        help_text = (
            "🤖 **Command List**\n\n"
            "💡 **Prefix:** `/`\n\n"
            "**Support Group:** @KoalaSuppot\n"
            "🎋 **Support us by following us on Instagram:**\n"
            "https://www.instagram.com/das_abae\n\n"
            "This help menu is designed to help you get started with the bot.\n\n"
        )

        emoji_map = {
            "General": "⚓",
            "Chat": "〽",
            "Game": "🎮",
            "Downloader": "📂",
            "Anime": "📗",
            "Economy": "👑",
        }

        for category, cmds in sorted(category_commands.items()):
            emoji = emoji_map.get(category, "📌")
            help_text += f"**{emoji} {category}**\n{format_cmds(cmds)}\n\n"

        help_text += (
            "📇 **Notes:**\n"
            "➛ Use `/help <command>` to get more info on a specific command.\n"
            "➛ For example: `/help profile`\n"
            "➛ `< >` means required, `[ ]` means optional — don't include them in actual usage.\n"
        )

        await self.client.send_message(M.chat_id, help_text)
