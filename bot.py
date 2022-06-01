import json
import typing

import dotenv
import nextcord
from nextcord.ext import commands

config: typing.Any = dotenv.dotenv_values(".env")

with open("guild_settings.json") as f:
    guilds = json.load(f)

intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

bot.load_extension("toolkit_menu")
bot.load_extension("settings_menu")
bot.load_extension("event_listeners")

@bot.slash_command(name="ping", guild_ids=[902859067708551230])
async def ping(interaction: nextcord.Interaction) -> None:
    print(guilds)
    await interaction.response.send_message("Pong from python")

bot.run(config["DISCORD_TOKEN"])