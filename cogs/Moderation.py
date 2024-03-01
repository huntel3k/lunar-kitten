import datetime

import disnake
from disnake.ext import commands


def convert_to_seconds(time, unit):
    if unit.lower() == 's':
        return time
    elif unit.lower() == 'm':
        return time * 60
    elif unit.lower() == 'h':
        return time * 3600
    elif unit.lower() == 'd':
        return time * 86400
    else:
        return None


def format_time(time_seconds):
    if time_seconds < 60:
        if time_seconds == 1:
            return time_seconds, "sekundę"
        elif time_seconds < 5:
            return time_seconds, "sekundy"
        else:
            return time_seconds, "sekund"
    elif time_seconds < 3600:
        if time_seconds == 60:
            return time_seconds // 60, "minutę"
        elif time_seconds < 300:
            return time_seconds // 60, "minuty"
        else:
            return time_seconds // 60, "minut"
    elif time_seconds < 86400:
        if time_seconds == 3600:
            return time_seconds // 3600, "godzinę"
        elif time_seconds < 18000:
            return time_seconds // 3600, "godziny"
        else:
            return time_seconds // 3600, "godzin"
    else:
        if time_seconds == 86400:
            return time_seconds // 86400, "dzień"
        else:
            return time_seconds // 86400, "dni"


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def is_user_banned(self, guild, user):
        bans = await guild.bans()
        return any(entry.user.id == user.id for entry in bans)

    @commands.slash_command(name='ban', description='Banuje wybranego użytkownika!')
    @commands.default_member_permissions(ban_members=True)
    async def ban_user(self, inter, user, reason: str = None):
            await inter.guild.ban(user, reason=reason)
            await inter.response.send_message(f"✔ Zbanowano **{user.mention}** z powodu {reason}",
                                                  ephemeral=True)

    @commands.slash_command(name='banlist', description='Pokazuje liste zbanowanych użytkowników!')
    @commands.default_member_permissions(ban_members=True)
    async def ban_list(self, inter):
        bans = await inter.guild.bans().flatten()
        if bans:
            banned_members = [f"\n {ban.user.name} (ID: {ban.user.id})" for ban in bans]
            thumbnail_url = 'https://cdn.discordapp.com/emojis/1036407994570776606.png?size=160&quality=lossless'
            embed = disnake.Embed(
                description=f"🛠 **Zbanowani użytkownicy:** {' '.join(banned_members)}",
                color=5420608
            )
            embed.set_thumbnail(url=thumbnail_url)
            await inter.response.send_message(embed=embed)
        else:
            embed = disnake.Embed(
                title=f"Nie ma zbanowanych użytkowników!.",
                color=6881294
            )
            await inter.response.send_message(embed=embed)

    @commands.slash_command(name='unban', description='Odbanuje wybranego użytkownika!')
    @commands.default_member_permissions(ban_members=True)
    async def unban_user(self, inter, user: disnake.User):
        # note: unban using <@id>
            await inter.guild.unban(user)
            await inter.response.send_message(f"✔ Odbanowano **{user.mention}**", ephemeral=True)

    @commands.slash_command(name='kick', description='Wyrzuca użytkownika z serwera!')
    @commands.default_member_permissions(kick_members=True)
    async def kick_user(self, inter, user: disnake.User, reason: str = None):
            try:
                await inter.guild.kick(user, reason=reason)
                await inter.response.send_message(f"✔ Wyrzucono **{user.mention}** z powodu {reason}",
                                                  ephemeral=True)
            except disnake.errors.Forbidden as e:
                await inter.response.send_message(f"❌ Nie udało się wyrzucić użytkownika: {e}", ephemeral=True)

    @commands.slash_command(name='mute', description='Wycisza wybranego użytkownika!')
    @commands.default_member_permissions(moderate_members=True)
    async def mute_user(self, inter, user: disnake.User, time: str, unit: str, reason: str):
        if isinstance(time, int):
            time_seconds = time
        else:
            # Convert time to string and filter digits
            time = ''.join(filter(str.isdigit, str(time)))

        # convert into seconds
        time = int(time)
        time_seconds = convert_to_seconds(int(time), unit)

        if time_seconds is None:
            await inter.response.send_message("❌ Nieprawidłowa jednostka czasu. Dostępne jednostki: s, m, h, d",
                                              ephemeral=True)
            return

        end_time = datetime.datetime.now() + datetime.timedelta(seconds=time_seconds)
        await user.timeout(reason=reason, until=end_time)

        if not time or not unit:
            await inter.response.send_message("❌ Podano nieprawidłowy format czasu.", ephemeral=True)
            return

        end_time = datetime.datetime.now() + datetime.timedelta(seconds=time_seconds)
        await user.timeout(reason=reason, until=end_time)
        if user.id == inter.author.id:
            await inter.response.send_message("❌ Nie mozesz wyciszyc siebie samego! :)", ephemeral=True)
            return
        else:
            pass
        formatted_time, unit_text = format_time(time_seconds)
        if time > 0:
            embed = disnake.Embed(
                description=f"🔇 **{user.name}** zostal wyciszony przez **{inter.author}**! na {formatted_time} {unit_text}, za {reason}",
                color=5420608
            )

            await inter.response.send_message(embed=embed)

        elif time == 0:
            embed = disnake.Embed(
                description=f"❌ Podano nieprawidłowa liczbe czasu!",
                color=6881294
            )
            await inter.response.send_message(embed=embed)

    @commands.slash_command(name='unmute', description='Odcisza wybranego użytkownika!')
    @commands.default_member_permissions(moderate_members=True)
    async def unmute_user(self, inter, user: disnake.User):
        await user.timeout(duration=None)
        embed = disnake.Embed(
            description=f"✔ Odciszono uzytkownika **{user.name}**!",
            color=6881294
        )
        await inter.response.send_message(embed=embed)

    @commands.slash_command(name='is_muted', description='Sprawdza czy dany użytkownik jest wyciszony.')
    @commands.default_member_permissions(moderate_members=True)
    async def is_muted_user(self, inter, user: disnake.User):
        can_send_messages = inter.channel.permissions_for(user).send_messages
        if not can_send_messages:
            embed = disnake.Embed(
                description=f"🔈 Użytkownik **{user.name}** jest wyciszony.",
                color=6881294
            )
            await inter.response.send_message(embed=embed)
        else:
            embed = disnake.Embed(
                description=f"🔇 Użytkownik **{user.name}** nie jest wyciszony.",
                color=5420608
            )
            await inter.response.send_message(embed=embed)

    @commands.slash_command(name='clear', description='Czysci podana ilosc wiadomosci.')
    @commands.default_member_permissions(ban_members=True)
    async def clear(self, inter, amount: int):
        try:
            if inter.author.guild_permissions.manage_messages:
                # Purge messages
                deleted_messages = await inter.channel.purge(limit=amount)

                if amount == 1:
                    await inter.response.send_message(
                        f"✔ Wyczyszczono {len(deleted_messages)} wiadomość!.", ephemeral=True
                    )
                else:
                    await inter.response.send_message(
                        f"✔ Wyczyszczono {len(deleted_messages)} wiadomości!.", ephemeral=True
                    )
            else:
                # Notify user about lack of permissions
                await inter.response.send_message(
                    "❌ Nie masz wystarczających uprawnień do usuwania wiadomości.", ephemeral=True
                )

        except disnake.NotFound:
            try:
                # If deferring fails, send a new message
                await inter.send(f"✔ Wyczyszczono {amount} wiadomości!.", ephemeral=True)
            except disnake.NotFound:
                # If sending a new message also fails, print an error
                print("❌ Wystąpił błąd: Unable to defer the response and send a new message.")
        except Exception as e:
            print(f"❌ Wystąpił błąd: {e}")

def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))
