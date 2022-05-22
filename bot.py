import os
import json
from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands

load_dotenv()

ORCA_SERVER_ID = 902859067708551230
channels_file = open("channels.json")
CHANNELS = json.load(channels_file)

intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

bot.load_extension("toolkit_menu")
bot.load_extension("settings_menu")

@bot.slash_command(name="ping", guild_ids=[ORCA_SERVER_ID])
async def ping(interaction: nextcord.Interaction):
    print(CHANNELS)
    await interaction.response.send_message("Pong from python")

async def send_admin_given_message(audit_logs, guild):
    channel = bot.get_channel(int(CHANNELS[str(guild.id)]["notification_channel"]))
    async for entry in audit_logs:
        await channel.send(f"""
        :bangbang: <@&933071056917364747>
        • {entry.user} turned __on__ **Administrator** permissions for the {entry.target} role
        • Check with ... to make sure this is not a security breach!
        """)

async def send_admin_taken_message(audit_logs, guild):
    channel = bot.get_channel(int(CHANNELS[str(guild.id)]["notification_channel"]))
    async for entry in audit_logs:
        await channel.send(f"""
        :bangbang: <@&933071056917364747>
        • {entry.user} turned __off__ Administrator permissions for the {entry.target} role
        • Check with ... to make sure this is not a security breach!
        """)

@bot.event
async def on_guild_role_update(before, after):
    guild = before.guild
    if not before.permissions.administrator and after.permissions.administrator:
        await send_admin_given_message(guild.audit_logs(limit=1), guild)
    if before.permissions.administrator and not after.permissions.administrator:
        await send_admin_taken_message(guild.audit_logs(limit=1), guild)

@bot.event
async def on_ready():
    print(f"{bot.user} is running...")

bot.run(os.getenv("DISCORD_TOKEN"))