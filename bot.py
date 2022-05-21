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

# @client.event
# async def on_message(msg):
#     await client.wait_until_ready()

#     if msg.author == client.user:
#         return

#     if msg.content.startswith("!boot-is-ready"):
#         await msg.channel.send("The Boot is ready!")

#     if msg.content.startswith("!boot-users-without-roles"):
#         n_kicked = 0
#         names_kicked = []
#         await msg.channel.send(f"Booting ALL users without a member role!")
#         for server in client.guilds:
#             for member in server.members:
#                 if len(member.roles) == 1:
#                     try:
#                         print(f"Attempting to kick {member.name}...")
#                         await asyncio.sleep(2.5)
#                         await server.kick(member, reason="No role after server sweep")
#                         names_kicked.append([member.name])
#                         n_kicked += 1
#                         continue
#                     except Exception as e:
#                         print(e)
#                         continue
#             await msg.channel.send(f"Succesfully kicked {n_kicked} from {server.name}")
#             print(f"Succesfully kicked {n_kicked} from {server.name}")
#         # Write to file
#         today = date.today()
#         t = today.strftime("%Y-%b-%d")
#         with open(f"boot-records/{t}.csv", "w") as f: 
#             write = csv.writer(f) 
#             write.writerows(names_kicked)

# client.run(os.getenv("DISCORD_TOKEN"))