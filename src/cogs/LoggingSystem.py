import datetime

import disnake
from disnake.ext import commands

timestamp = datetime.datetime.now(datetime.UTC)
unix_timestamp = int(timestamp.timestamp())
format_timestamp = f"<t:{unix_timestamp}:F>"


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel = None
        self.bot.loop.create_task(self.setup_log_channel())

    async def setup_log_channel(self):
        await self.bot.wait_until_ready()

        guild = disnake.utils.get(self.bot.guilds)
        if guild:
            self.log_channel = disnake.utils.get(guild.text_channels, name="off-topic")
            print(f"Log channel set to: {self.log_channel.name if self.log_channel else 'None'}")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        if self.log_channel is None:
            return

        deleted_embed = disnake.Embed(title="Usunięto wiadomość",
                                      color=disnake.Color.red())
        deleted_embed.add_field(name="Autor:", value=message.author.mention)
        deleted_embed.add_field(name="Kanał:", value=message.channel.mention)
        deleted_embed.add_field(name="Zawartość:", value=f"`{message.content}`", inline=False)
        deleted_embed.add_field(name="Czas usunięcia:", value=format_timestamp, inline=False)
        deleted_embed.set_footer(text=f"ID: {message.id}")

        await self.log_channel.send(embed=deleted_embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return

        if self.log_channel is None:
            return

        message_link = f"https://discord.com/channels/{after.guild.id}/{after.channel.id}/{after.id}"

        edited_embed = disnake.Embed(description=f"[**Zmodyfikowano wiadomość**]({message_link})",
                                     color=disnake.Color.orange())

        edited_embed.add_field(name="Autor:", value=after.author.mention)
        edited_embed.add_field(name="Kanał:", value=after.channel.mention)
        edited_embed.add_field(name="Zawartość przed:", value=f"`{before.content}`", inline=False)
        edited_embed.add_field(name="Zawartość po:", value=f"`{after.content}`", inline=False)
        edited_embed.add_field(name="Czas zmodyfikowania:", value=format_timestamp, inline=False)
        edited_embed.set_footer(text=f"ID: {after.id}")

        await self.log_channel.send(embed=edited_embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):

        if self.log_channel is None:
            return

        # Create an embed to log the channel creation
        created_embed = disnake.Embed(title=f"Nowy kanał utworzony !",
                                      color=disnake.Color.green())

        created_embed.add_field(name="Kanał:", value=channel.mention)
        created_embed.add_field(name="Typ kanału:", value=str(channel.type).capitalize())
        created_embed.add_field(name="Czas stworzenia:", value=format_timestamp, inline=False)
        created_embed.set_footer(text=f"ID: {channel.id}")

        await self.log_channel.send(embed=created_embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):

        if self.log_channel is None:
            return

        # Create an embed to log the channel deletion
        deleted_embed = disnake.Embed(title=f"Usunięto kanał !",
                                      color=disnake.Color.red())

        deleted_embed.add_field(name="Kanał:", value=f"#{channel.name}")
        deleted_embed.add_field(name="Czas stworzenia:", value=format_timestamp)
        deleted_embed.set_footer(text=f"ID: {channel.id}")

        await self.log_channel.send(embed=deleted_embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):

        # Retrieve audit logs to find who banned the user, when, and the reason
        async for entry in guild.audit_logs(action=disnake.AuditLogAction.ban, limit=1):
            if entry.target.id == user.id:
                banned_by = entry.user
                ban_time = entry.created_at
                reason = entry.reason
                break
        else:
            banned_by = None
            ban_time = None
            reason = 'No reason provided'

        # Create an embed to log the member banning
        ban_embed = disnake.Embed(
            title="User Banned",
            description=f"**User Banned:** {user.mention}\n"
                        f"**Banned By:** {banned_by.mention if banned_by else 'Unknown'}\n"
                        f"**Ban Time:** <t:{int(ban_time.timestamp())}>\n"
                        f"**Reason:** {reason if reason else 'No reason provided'}",
            color=disnake.Color.red()
        )
        ban_embed.set_footer(text=f"User ID: {user.id}")

        await self.log_channel.send(embed=ban_embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):

        # Retrieve audit logs to find who unbanned the user and when
        async for entry in guild.audit_logs(action=disnake.AuditLogAction.unban, limit=1):
            if entry.target.id == user.id:
                unbanned_by = entry.user
                unban_time = entry.created_at
                reason = entry.reason
                break
        else:
            unbanned_by = None
            unban_time = None
            reason = 'No reason provided'

        # Create an embed to log the member unbanning
        unban_embed = disnake.Embed(
            title="User Unbanned",
            description=f"**User Unbanned:** {user.mention}\n"
                        f"**Unbanned By:** {unbanned_by.mention if unbanned_by else 'Unknown'}\n"
                        f"**Unban Time:** <t:{int(unban_time.timestamp())}>\n"
                        f"**Reason:** {reason if reason else 'No reason provided'}",
            color=disnake.Color.green()
        )
        unban_embed.set_footer(text=f"User ID: {user.id}")

        await self.log_channel.send(embed=unban_embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):

        if self.log_channel is None:
            return

        # Create an embed to log the member joining
        welcome_embed = disnake.Embed(
            description=f"Witaj na lunar kitten beta preview, {member.mention}",
            color=disnake.Color.dark_green()
        )
        welcome_embed.set_footer(text=f"ID: {member.id}")

        await self.log_channel.send(embed=welcome_embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        if self.log_channel is None:
            return

        # Create an embed to log the member leaving
        goodbye_embed = disnake.Embed(
            description=f"{member.mention} właśnie opuścił serwer !",
            color=disnake.Color.dark_red()
        )
        goodbye_embed.set_footer(text=f"ID: {member.id}")

        await self.log_channel.send(embed=goodbye_embed)


def setup(bot: commands.Bot):
    bot.add_cog(Logging(bot))
