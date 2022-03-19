import discord
import os
import asyncio
import csv
from discord.ext import commands
from dotenv import load_dotenv
from datetime import date

load_dotenv()

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="", intents=intents)

@client.event
async def on_ready():
    print("Ready...")

@client.event
async def on_message(msg):
    await client.wait_until_ready()

    if msg.author == client.user:
        return

    if msg.content.startswith("!boot-users-without-roles"):
        n_kicked = 0
        names_kicked = []
        print("Sweeping server...")
        for server in client.guilds:
            for member in server.members:
                if len(member.roles) == 1:
                    try:
                        print(f"Attempting to kick {member.name}...")
                        await asyncio.sleep(2.5)
                        await server.kick(member, reason="No role after server sweep")
                        names_kicked.append([member.name])
                        n_kicked += 1
                        continue
                    except Exception as e:
                        print(e)
                        continue
        # Write to file
        today = date.today()
        t = today.strftime("%Y-%b-%d")
        with open(f"boot-records/{t}.csv", "w") as f: 
            write = csv.writer(f) 
            write.writerows(names_kicked) 
        print(f"Succesfully kicked {n_kicked} from {server.name}")

client.run(os.getenv("DISCORD_TOKEN"))