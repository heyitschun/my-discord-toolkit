from datetime import datetime, timezone

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from bot import bot, ORCA_SERVER_ID

class Dropdown(nextcord.ui.Select):
    def __init__(self, bot):
        self.guild = bot.get_guild(ORCA_SERVER_ID)
        options = [
            nextcord.SelectOption(label="0: Purgeable members (no role after 14 days)"),
            nextcord.SelectOption(label="1: Who has admin permissions?"),
        ]
        super().__init__(
            placeholder="Select something to do...", 
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: Interaction):

        # count how many members have no role after 21 days of joining
        if self.values[0].startswith("0"):
            purgeable = {}
            for member in self.guild.members:
                days_since_joining = (datetime.now(timezone.utc) - member.joined_at).days
                if len(member.roles) == 1 and days_since_joining > 21:
                    purgeable[member.name] = {"days_since_joining": days_since_joining}
            return await interaction.response.send_message(f"Nr of users who failed to become a member within 21 days: {len(purgeable.keys())}")

        # check which members have admin permissions
        if self.values[0].startswith("1"):
            admin_roles = [role for role in self.guild.roles if role.permissions.administrator]
            bot_admins = [] 
            human_admins = []
            for ar in admin_roles:
                for member in ar.members:
                    if member.bot:
                        bot_admins.append(str(member))
                    else:
                        human_admins.append(str(member))
            bot_admin_message = "\n".join(bot_admins)
            human_admin_message = "\n".join(human_admins)
            return await interaction.response.send_message(f"The following members have admin permissions:\n\n__Bots__\n{bot_admin_message}\n\n__Humans__\n{human_admin_message}")

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

class DropdownView(nextcord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        self.add_item(Dropdown(self.bot))

class ToolkitMenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.slash_command(name="ctk", guild_ids=[ORCA_SERVER_ID])
    @commands.has_permissions(administrator=True)
    async def chuns_toolkit(self, ctx):
        view = DropdownView(self.bot)
        await ctx.send("", view=view)

def setup(bot):
    bot.add_cog(ToolkitMenuCog(bot))
