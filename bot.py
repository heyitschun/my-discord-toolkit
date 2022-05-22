import json

import dotenv
import nextcord
from nextcord.ext import commands

config = dotenv.dotenv_values(".env")

ORCA_SERVER_ID = 902859067708551230
GUILDS = json.load(open("guild_settings.json"))

intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

bot.load_extension("toolkit_menu")
bot.load_extension("settings_menu")
bot.load_extension("event_listeners")

@bot.slash_command(name="ping", guild_ids=[ORCA_SERVER_ID])
async def ping(interaction: nextcord.Interaction):
    print(GUILDS)
    await interaction.response.send_message("Pong from python")

bot.run(config["DISCORD_TOKEN"])