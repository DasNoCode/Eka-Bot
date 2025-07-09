from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "weather",
                "category": "general",
                "xp": True,
                "AdminOnly": False,
                "OwnerOnly": False,
                "ChatOnly": False,
                "description": {
                    "content": "Get the current weather for a location.",
                    "usage": "`/weather <location>` — Shows weather info for the given location."
                },
            },
        )

    async def exec(self, M: Message, context):
        if not context[3]:
            return await self.client.send_message(
                M.chat_id, "/weather your location"
            )

        location = " ".join(M.message[1:])

        try:
            response = self.client.utils.fetch(f"https://wttr.in/{location}?format=j1")

            current = response['current_condition'][0]
            weather_report = (
                f"🌤️  **{location.title()}**\n"
                f"🌡️ **Temperature:** {current['temp_C']}°C (Feels like {current['FeelsLikeC']}°C)\n"
                f"🌫️ **Condition:** {current['weatherDesc'][0]['value']}\n"
                f"💨 **Wind:** {current['windspeedKmph']} km/h {current['winddir16Point']}\n"
                f"💧 **Humidity:** {current['humidity']}%\n"
                f"🌧️ **Precipitation:** {current['precipMM']} mm"
            )
            
            await self.client.send_message(M.chat_id, weather_report)
        except Exception as error:
            self.client.log.error(str(error))
            await self.client.send_message(M.chat_id, f"**Error occurred:** {error}")
