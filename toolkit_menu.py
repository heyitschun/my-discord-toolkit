import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from bot import bot, ORCA_SERVER_ID

class Dropdown(nextcord.ui.Select):
    def __init__(self, bot):
        self.guild = bot.get_guild(ORCA_SERVER_ID)
        options = [
            nextcord.SelectOption(label="Who has admin permissions?"),
        ]
        super().__init__(
            placeholder="Select something to do...", 
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: Interaction):
        # See which members have admin permissions
        if self.values[0] == "Who has admin permissions?":
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
