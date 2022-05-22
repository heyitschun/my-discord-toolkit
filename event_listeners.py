import typing
import json

import nextcord
from nextcord.ext import commands

from bot import bot

async def on_ready() -> None:
    print(f"\n{bot.user} is online...\n")

async def send_role_update_message_to_admin(
        guild: nextcord.Guild,
        changed_permission: str,
        new_permission_value: bool
    ) -> None:
    with open("guild_settings.json") as f:
        guilds = json.load(f)
    admin_id = guilds[str(guild.id)]["admin_role_id"]
    channel: typing.Any = bot.get_channel(int(guilds[str(guild.id)]["notification_channel"]))
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
    ) -> None:
    with open("guild_settings.json") as f:
        guilds = json.load(f)
    channel: typing.Any = bot.get_channel(int(guilds[str(guild.id)]["notification_channel"]))
    entry: nextcord.audit_logs.AuditLogEntry
    async for entry in guild.audit_logs(limit=1):
        await channel.send(f"""**Permissions update**
            • {entry.user} set {changed_permission} for {entry.target} to {new_permission_value}
        """)

async def on_guild_role_update(before: nextcord.Role, after: nextcord.Role) -> None:
    """Listen to critical permission changes."""
    guild = before.guild
    
    if not before.permissions.administrator and after.permissions.administrator:
        await send_role_update_message_to_admin(guild, "Administrator", after.permissions.administrator)
    elif before.permissions.administrator and not after.permissions.administrator:
        await send_role_update_message_to_admin(guild, "Administrator", after.permissions.administrator)
    
    if not before.permissions.manage_guild and after.permissions.manage_guild:
        await send_role_update_message(guild, "Manage Server", after.permissions.manage_guild)
    elif before.permissions.manage_guild and not after.permissions.manage_guild:
        await send_role_update_message(guild, "Manage Server", after.permissions.manage_guild)

async def on_member_join(member: nextcord.Member) -> None:
    """Check if new joiner is on the blacklist. If so, ban them."""
    with open("guild_settings.json") as f:
        guilds = json.load(f)
    blacklist = guilds[str(member.guild.id)]["blacklist"]
    is_blacklisted = str(member.id) in blacklist
    if is_blacklisted:
        channel: typing.Any = bot.get_channel(int(guilds[str(member.guild.id)]["notification_channel"]))
        try:
            await member.ban(delete_message_days=7, reason="Blacklisted")
            await channel.send(f"""**Blacklisted user detected!**
                • A blacklisted user tried to join and has been banned from the server.
                • User ID: @{member.id}
            """)
        except Exception:
            await channel.send(f"""**Blacklisted user detected!**
                • A blacklisted user joined the server, but CTK failed to ban them.
                • User ID: <@{member.id}>
            """)

def setup(bot: commands.Bot):
    bot.add_listener(on_ready)
    bot.add_listener(on_guild_role_update)
    bot.add_listener(on_member_join)