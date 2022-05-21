import json
import nextcord
from nextcord.ext import commands

from bot import bot, ORCA_SERVER_ID

class SettingsModal(nextcord.ui.Modal):
    def __init__(self, interaction):
        f = open("channels.json")
        self.channels = json.load(f)
        self.channel_settings = self.channels[str(interaction.guild_id)]
        super().__init__(
            "Chun's Toolkit Settings",
            timeout=5 * 60,  # 5 minutes
        )

        self.notification_channel = nextcord.ui.TextInput(
            label="Channel to send notifications to (ChannelID)",
            min_length=2,
            max_length=50,
            placeholder=self.channel_settings["notification_channel"],
            required=False
        )
        self.add_item(self.notification_channel)

        self.admin_role_id = nextcord.ui.TextInput(
            label="Server admin role ID",
            min_length=2,
            max_length=50,
            placeholder=self.channel_settings["admin_role_id"],
            required=False
        )
        self.add_item(self.admin_role_id)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        response = f"""
            Notification channel: <#{self.notification_channel.value}>.
            Server admin: <@&{self.admin_role_id.value}>
        """
        save_data = {
            "notification_channel": self.notification_channel.value,
            "admin_role_id.value": self.admin_role_id.value
        }
        self.channels[interaction.guild_id] = save_data
        new_json = json.dumps(self.channels)
        with open("channels.json", "w") as out:
            out.write(new_json)
            out.close()
        await interaction.response.send_message(response, ephemeral=True)