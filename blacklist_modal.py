import json

import nextcord
from nextcord import Interaction

from bot import GUILDS

class BlacklistModal(nextcord.ui.Modal):
    def __init__(self, interaction: Interaction):
        self.guilds = GUILDS
        super().__init__(
            "Add user ID to blacklist",
            timeout = 5*60 # 5 minutes
        )

        self.add_to_blacklist = nextcord.ui.TextInput(
            custom_id="add_to_blacklist",
            label="Enter user's ID to blacklist them",
            min_length=2,
            max_length=50,
            required=True
        )
        self.add_item(self.add_to_blacklist)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        self.guilds[str(interaction.guild_id)]["blacklist"].append(self.add_to_blacklist.value)
        # save to json
        with open("guild_settings.json", "w") as out:
            json.dump(self.guilds, out, indent=2)
            out.close()

        response = f"""**Blacklist updated**
        • User with ID @{self.add_to_blacklist.value} has been added to this server's blacklist.
        • They will be banned now or, if they aren't in this server yet, will be banned as soon as they try to join.
        """
        await interaction.response.send_message(response, ephemeral=True)