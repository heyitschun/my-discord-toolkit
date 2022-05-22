import typing

import nextcord
from nextcord.ext import commands

from bot import bot, GUILDS

async def on_ready() -> None:
    print(f"\n{bot.user} is online...\n")

async def send_role_update_message_to_admin(
        guild: nextcord.Guild,
        changed_permission: str,
        new_permission_value: bool
    ):
    admin_id = GUILDS[str(guild.id)]["admin_role_id"]
    channel: typing.Any = bot.get_channel(int(GUILDS[str(guild.id)]["notification_channel"]))
    entry: nextcord.audit_logs.AuditLogEntry
    async for entry in guild.audit_logs(limit=1):
        await channel.send(f"""<@&{admin_id}>: **Administrator update**
            • {entry.user} set {changed_permission} for {entry.target} to {new_permission_value}
            • Check with ... to make sure this is not a security breach!
        """)

async def send_role_update_message(
        guild: nextcord.Guild,
        changed_permission: str,
        new_permission_value: bool
    ):
    channel: typing.Any = bot.get_channel(int(GUILDS[str(guild.id)]["notification_channel"]))
    entry: nextcord.audit_logs.AuditLogEntry
    async for entry in guild.audit_logs(limit=1):
        await channel.send(f"""**Permissions update**
            • {entry.user} set {changed_permission} for {entry.target} to {new_permission_value}
        """)

async def on_guild_role_update(before: nextcord.Role, after: nextcord.Role):
    guild = before.guild
    if not before.permissions.administrator and after.permissions.administrator:
        await send_role_update_message_to_admin(guild, "Administrator", after.permissions.administrator)
    elif before.permissions.administrator and not after.permissions.administrator:
        await send_role_update_message_to_admin(guild, "Administrator", after.permissions.administrator)
    elif not before.permissions.manage_guild and after.permissions.manage_guild:
        await send_role_update_message(guild, "Manage Server", after.permissions.manage_guild)
    elif before.permissions.manage_guild and not after.permissions.manage_guild:
        await send_role_update_message(guild, "Manage Server", after.permissions.manage_guild)

def setup(bot: commands.Bot):
    bot.add_listener(on_ready)
    bot.add_listener(on_guild_role_update)