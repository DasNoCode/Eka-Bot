import aiohttp

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "git",
                "category": "general",
                "xp": True,
                "AdminOnly": False,
                "OwnerOnly": False,
                "ChatOnly": False,
                "description": {
                    "content": "Fetch GitHub user profile and repositories.",
                    "usage": "/git username — returns GitHub bio, creation date, company, and top repos."
                },
            },
        )

    async def exec(self, message: Message, context):
        if len(message.message.split()) == 1:
            return await self.client.send_message(
                message.chat_id, "❌ Usage: `/git username`"
            )

        username = message.message.split(None, 1)[1]
        user_url = f"https://api.github.com/users/{username}"

        async with aiohttp.ClientSession() as session:
            async with session.get(user_url) as user_response:
                if user_response.status == 404:
                    return await self.client.send_message(
                        message.chat_id,
                        f"❌ GitHub user `{username}` not found.",
                    )

                user_data = await user_response.json()

                html_url = user_data.get("html_url", "N/A")
                name = user_data.get("name", "N/A")
                company = user_data.get("company", "N/A")
                bio = user_data.get("bio", "N/A")
                created_at = user_data.get("created_at", "N/A")
                repos_url = user_data.get("repos_url")

                response_text = (
                    "🧑‍💻  **GitHub User Info**\n\n"
                    f"**Username:** `{username}`\n"
                    f"**Name:** {name or 'N/A'}\n"
                    f"**Bio:** {bio or 'N/A'}\n"
                    f"**Company:** {company or 'N/A'}\n"
                    f"**Created:** {created_at}\n"
                    f"🔗 **URL**: [Profile Link]({html_url})\n\n"
                )

                if repos_url:
                    async with session.get(repos_url) as repo_response:
                        if repo_response.status != 200:
                            return await self.client.send_message(message.chat_id, response_text)

                        repos = await repo_response.json()
                        if repos:
                            response_text += "📦 **Top Repositories:**\n"
                            for idx, repo in enumerate(repos[:5], start=1):
                                repo_name = repo.get("name")
                                repo_link = repo.get("html_url")
                                response_text += f"[{idx}. {repo_name}]({repo_link})\n"

                await self.client.send_message(message.chat_id, response_text, disable_web_page_preview=True)
