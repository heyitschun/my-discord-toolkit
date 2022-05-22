from nextcord import Interaction
from nextcord.ext import commands

from bot import bot, ORCA_SERVER_ID
from settings_modal import SettingsModal

class SettingsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @bot.slash_command(
        name="ctk-settings",
        description="Chun's Toolkit Settings",
        guild_ids=[ORCA_SERVER_ID],
    )
    async def settings(self, interaction: Interaction):
        modal = SettingsModal(interaction)
        await interaction.response.send_modal(modal)

def setup(bot: commands.Bot):
    bot.add_cog(SettingsCog(bot))