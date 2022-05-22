import typing

import nextcord
from nextcord.ext import commands
from nextcord.iterators import AuditLogIterator

from bot import bot, GUILDS

async def on_ready() -> None:
    print(f"\n{bot.user} is running...\n")

async def send_admin_given_message(audit_logs: AuditLogIterator, guild: nextcord.Guild):
    channel: typing.Any = bot.get_channel(int(GUILDS[str(guild.id)]["notification_channel"]))
    entry: nextcord.audit_logs.AuditLogEntry
    async for entry in audit_logs:
        await channel.send(f"""
        :bangbang: <@&933071056917364747>
        • {entry.user} turned __on__ **Administrator** permissions for the {entry.target} role
        • Check with ... to make sure this is not a security breach!
        """)

async def send_admin_taken_message(audit_logs: AuditLogIterator, guild: nextcord.Guild):
    channel: typing.Any = bot.get_channel(int(GUILDS[str(guild.id)]["notification_channel"]))
    entry: nextcord.audit_logs.AuditLogEntry
    async for entry in audit_logs:
        await channel.send(f"""
        :bangbang: <@&933071056917364747>
        • {entry.user} turned __off__ Administrator permissions for the {entry.target} role
        • Check with ... to make sure this is not a security breach!
        """)

async def on_guild_role_update(before: nextcord.Role, after: nextcord.Role):
    guild = before.guild
    if not before.permissions.administrator and after.permissions.administrator:
        await send_admin_given_message(guild.audit_logs(limit=1), guild)
    if before.permissions.administrator and not after.permissions.administrator:
        await send_admin_taken_message(guild.audit_logs(limit=1), guild)

def setup(bot: commands.Bot):
    bot.add_listener(on_ready)
    bot.add_listener(on_guild_role_update)