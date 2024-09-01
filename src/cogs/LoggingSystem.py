import disnake
from disnake.ext import commands


class Logging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return

        log_channel = disnake.utils.get(message.guild.text_channels, name='nasze-boty')

        if log_channel is None:
            return  # Log channel not found

        # Create a hoverable timestamp using the Unix timestamp
        timestamp = int(message.created_at.timestamp())
        formatted_time = f"<t:{timestamp}:F>"

        deleted_embed = disnake.Embed(title="Usunięto wiadomość",
                                      color=disnake.Color.red(),
                                      timestamp=disnake.utils.utcnow())
        deleted_embed.add_field(name="Autor:", value=message.author.mention, inline=True)
        deleted_embed.add_field(name="Kanał:", value=message.channel.mention, inline=True)
        deleted_embed.add_field(name="Zawartość:", value=f"`{message.content}`", inline=False)
        deleted_embed.add_field(name="Czas:", value=formatted_time, inline=False)
        deleted_embed.set_footer(text=f"ID: {message.id}")

        await log_channel.send(embed=deleted_embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author == self.bot.user:
            return

        log_channel = disnake.utils.get(after.guild.text_channels, name='nasze-boty')

        if log_channel is None:
            return

        timestamp = int(after.created_at.timestamp())
        formatted_time = f"<t:{timestamp}:F>"

        edited_embed = disnake.Embed(title="Zmodyfikowano wiadomość",
                                     color=disnake.Color.orange(),
                                     timestamp=disnake.utils.utcnow())
        edited_embed.add_field(name="Autor:", value=after.author.mention, inline=True)
        edited_embed.add_field(name="Kanał:", value=after.channel.mention, inline=True)
        edited_embed.add_field(name="Zawartość przed:", value=f"`{before.content}`", inline=False)
        edited_embed.add_field(name="Zawartość po:", value=f"`{after.content}`", inline=False)
        edited_embed.add_field(name="Czas:", value=formatted_time, inline=False)
        edited_embed.set_footer(text=f"ID: {after.id}")

        await log_channel.send(embed=edited_embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        log_channel = disnake.utils.get(channel.guild.text_channels, name='nasze-boty')

        if log_channel is None:
            return

        timestamp = int(channel.created_at.timestamp())
        formatted_time = f"<t:{timestamp}:F>"

        # Create an embed to log the channel creation
        created_embed = disnake.Embed(title=f"Nowy kanał utworzony !",
                                      color=disnake.Color.green(),
                                      timestamp=disnake.utils.utcnow())
        created_embed.add_field(name="Kanał:", value=channel.mention, inline=True)
        created_embed.add_field(name="Typ kanału:", value=str(channel.type).capitalize(), inline=True)
        created_embed.add_field(name="Czas stworzenia:", value=formatted_time, inline=False)
        created_embed.set_footer(text=f"ID: {channel.id}")

        await log_channel.send(embed=created_embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        log_channel = disnake.utils.get(channel.guild.text_channels, name='nasze-boty')

        if log_channel is None:
            return

        timestamp = int(channel.created_at.timestamp())
        formatted_time = f"<t:{timestamp}:F>"

        # Create an embed to log the channel deletion
        deleted_embed = disnake.Embed(title=f"Usunięto kanał !",
                                      color=disnake.Color.red(),
                                      timestamp=disnake.utils.utcnow())
        deleted_embed.add_field(name="Kanał:", value=f"#{channel.name}", inline=True)
        deleted_embed.add_field(name="Czas stworzenia:", value=formatted_time, inline=True)
        deleted_embed.set_footer(text=f"ID: {channel.id}")

        await log_channel.send(embed=deleted_embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        log_channel = disnake.utils.get(guild.text_channels, name='nasze-boty')

        if log_channel is None:
            return

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

        await log_channel.send(embed=ban_embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        log_channel = disnake.utils.get(guild.text_channels, name='nasze-boty')

        if log_channel is None:
            return

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

        await log_channel.send(embed=unban_embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        log_channel = disnake.utils.get(member.guild.text_channels, name='nasze-boty')

        if log_channel is None:
            return

        # Create an embed to log the member joining
        welcome_embed = disnake.Embed(
            description=f"Witaj na lunar kitten beta preview, {member.mention}",
            color=disnake.Color.dark_green()
        )
        welcome_embed.set_footer(text=f"ID: {member.id}")

        await log_channel.send(embed=welcome_embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log_channel = disnake.utils.get(member.guild.text_channels, name='nasze-boty')

        if log_channel is None:
            return

        # Create an embed to log the member leaving
        goodbye_embed = disnake.Embed(
            description=f"{member.mention} właśnie opuścił serwer !",
            color=disnake.Color.dark_red()
        )
        goodbye_embed.set_footer(text=f"ID: {member.id}")

        await log_channel.send(embed=goodbye_embed)


def setup(bot: commands.Bot):
    bot.add_cog(Logging(bot))
