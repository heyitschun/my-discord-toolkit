import json

import nextcord
from nextcord import Interaction

from bot import GUILDS

class SettingsModal(nextcord.ui.Modal):
    def __init__(self, interaction: Interaction):
        # f = open("guild_settings.json")
        # self.guilds = json.load(f)
        self.guilds = GUILDS
        super().__init__(
            "Chun's Toolkit Settings",
            timeout=5 * 60,  # 5 minutes
        )

        self.notification_channel = nextcord.ui.TextInput(
            custom_id="notification_channel",
            label="Channel to send notifications to (ChannelID)",
            min_length=2,
            max_length=50,
            default_value=self.guilds[str(interaction.guild_id)]["notification_channel"],
            placeholder=self.guilds[str(interaction.guild_id)]["notification_channel"],
            required=False
        )
        self.add_item(self.notification_channel)

        self.admin_role_id = nextcord.ui.TextInput(
            custom_id="admin_role_id",
            label="Server admin role ID",
            min_length=2,
            max_length=50,
            default_value=self.guilds[str(interaction.guild_id)]["admin_role_id"],
            placeholder=self.guilds[str(interaction.guild_id)]["admin_role_id"],
            required=False
        )
        self.add_item(self.admin_role_id)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        for child in self.children:
            self.guilds[str(interaction.guild_id)][child.custom_id] = child.value #type:ignore
        # save to json
        with open("guild_settings.json", "w") as out:
            json.dump(self.guilds, out, indent=2)
            out.close()

        response = f"""**Settings updated**
            • Notification channel: <#{self.notification_channel.value}>.
            • Server admin: <@&{self.admin_role_id.value}>
        """
        await interaction.response.send_message(response, ephemeral=True)


