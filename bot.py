import json

import dotenv
import nextcord
from nextcord.ext import commands

config = dotenv.dotenv_values(".env")

with open("guild_settings.json") as f:
    guilds = json.load(f)

intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

bot.load_extension("toolkit_menu")
bot.load_extension("settings_menu")
bot.load_extension("event_listeners")

@bot.slash_command(name="ping")
async def ping(interaction: nextcord.Interaction):
    print(guilds)
    await interaction.response.send_message("Pong from python")

bot.run(config["DISCORD_TOKEN"])