from disnake.ext import commands
import disnake
# future plan change it into embed
class BanKickAndUnbanUser(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def check_permissions_ban(self, interaction):
        return interaction.author.guild_permissions.ban_members
    async def check_permissions_kick(self, interaction):
        return interaction.author.guild_permissions.kick_members

    async def is_user_banned(self, guild, user):
        bans = await guild.bans()
        return any(entry.user.id == user.id for entry in bans)

    @commands.slash_command(name="ban", description='Zbanuj użytkownika!')
    async def ban(self, inter, user: disnake.User, reason: str):
        # Check permissions before attempting to ban
        if await self.check_permissions_ban(inter):
            try:
                await inter.guild.ban(user, reason=reason)
                await inter.response.send_message(f"✔ Zbanowano **{user.mention}** z powodu {reason}", ephemeral=True)
            except disnake.errors.Forbidden as e:
                await inter.response.send_message(f"❌ Nie udało się zbanować użytkownika: {e}", ephemeral=True)
        else:
            await inter.response.send_message(
                "❌ Nie masz uprawnień do zbanowania użytkownika!",
                ephemeral=True
            )

    @commands.slash_command(name="banlist", description='Sprawdz listę zbanowanych użytkoników', help='Sprawdz listę zbanowanych użytkoników')
    async def banlist(self, inter):
        if inter.author.guild_permissions.ban_members:
            bans = await inter.guild.bans().flatten()
            if bans:
                banned_members = [f"\n {ban.user.name} (ID: {ban.user.id})" for ban in bans]
                thumbnail_url = 'https://cdn.discordapp.com/emojis/1036407994570776606.png?size=160&quality=lossless'
                embed = disnake.Embed(
                    description=f"🛠 Zbanowani użytkownicy: {' '.join(banned_members)}",
                    color=5420608
                )
                embed.set_thumbnail(url=thumbnail_url)
                await inter.response.send_message(embed=embed)
            else:
                embed = disnake.Embed(
                    description=f"Nie ma zbanowanych użytkowników!.",
                    color=6881294
                )
                await inter.response.send_message(embed=embed)
        else:
            embed = disnake.Embed(
                description=f"❌ Nie masz permisji aby użyć tej komendy!",
                color=6881294
            )
            await inter.response.send_message(embed=embed)

    @commands.slash_command(name="kick", description='Wyrzuc użytkownika!')
    async def kick(self, inter, user: disnake.User, reason: str):
        # Check permissions before attempting to kick
        if await self.check_permissions_kick(inter):
            try:
                await inter.guild.kick(user, reason=reason)
                await inter.response.send_message(f"✔ Wyrzucono **{user.mention}** z powodu {reason}", ephemeral=True)
            except disnake.errors.Forbidden as e:
                await inter.response.send_message(f"❌ Nie udało się wyrzucić użytkownika: {e}", ephemeral=True)
        else:
            await inter.response.send_message(
                "❌ Nie masz uprawnień do wyrzucania użytkownikow!",
                ephemeral=True
                )
    @commands.slash_command(name="unban", description="Odbanuj członka!")
    async def unban(self, interaction, user: disnake.User):
        # Check permissions before attempting to unban
        # note: unban using <@id>
        if await self.check_permissions_ban(interaction):
            await interaction.guild.unban(user)
            await interaction.response.send_message(f"✔ Odbanowano **{user.mention}**", ephemeral=True)
        else:
            await interaction.response.send_message(
                "❌ Nie masz uprawnień do odbanowania użytkownika!",
                ephemeral=True
            )

def setup(bot: commands.Bot):
    bot.add_cog(BanKickAndUnbanUser(bot))
