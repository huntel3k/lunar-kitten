from datetime import timedelta

import disnake
from disnake.ext import commands

from src.utils.unitconverter import convert_time_to_seconds


class Moderation(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="moderation")
    async def moderation(self, inter: disnake.ApplicationCommandInteraction):
        pass

    @moderation.sub_command(name="ban", description="Banuje użytkownika z serwera!")
    async def ban(self, inter: disnake.ApplicationCommandInteraction,
                  user: disnake.Member, reason: str = "No reason provided."):
        bansuccess = disnake.Embed(title="✅ Sukces",
                                   description=f"`Pomyślnie zbanowano użytkownika:` {user.mention}\n "
                                               f"`Powod:` *{reason}*",
                                   color=disnake.Color.green(),
                                   timestamp=disnake.utils.utcnow())

        mentioneduserbanfailure = disnake.Embed(title="⚠️ Nie udało się zbanować tego użytkownika !",
                                                description=f"`{user.name} ma uprawnienia do banowania !`",
                                                color=disnake.Color.red(),
                                                timestamp=disnake.utils.utcnow())

        authorbanfailure = disnake.Embed(title="️⚠️ Nie udało się zbanować tego użytkownika !",
                                         description="*Nie możesz zbanować samego siebie*",
                                         color=disnake.Color.red(),
                                         timestamp=disnake.utils.utcnow())
        if user != inter.author:
            if user.guild_permissions.ban_members:
                await inter.response.send_message(embed=mentioneduserbanfailure)
            else:
                await inter.guild.ban(user, reason=reason)
                await inter.response.send_message(embed=bansuccess)
        else:
            await inter.response.send_message(embed=authorbanfailure)

    @ban.error
    async def moderation_error(self, inter: disnake.ApplicationCommandInteraction, error):
        if isinstance(error, commands.MissingPermissions):
            missingpermsforbaning = disnake.Embed(title="⚠️ Brak permisji !",
                                                  description=f"`{error}`",
                                                  color=disnake.Color.red(),
                                                  timestamp=disnake.utils.utcnow())
            await inter.response.send_message(embed=missingpermsforbaning)

        if isinstance(error, commands.UserNotFound):
            usernotfound = disnake.Embed(title="⚠️ Nie znaleziono użytkownika !",
                                         description=f"`{error}`",
                                         color=disnake.Color.red(),
                                         timestamp=disnake.utils.utcnow())
            await inter.response.send_message(embed=usernotfound)

    @moderation.sub_command(name="kick", description="Wyrzuca użytkownika z serwera!")
    async def kick(self, inter: disnake.ApplicationCommandInteraction,
                   user: disnake.Member, reason: str = "No reason provided."):
        kicksuccess = disnake.Embed(title="✅ Sukces",
                                    description=f"`Pomyślnie wyrzucono:` {user.mention}\n "
                                                f"`Powod:` *{reason}*",
                                    color=disnake.Color.green(),
                                    timestamp=disnake.utils.utcnow())

        mentioneduserkickfailure = disnake.Embed(title="⚠️ Nie udało się wyrzucić tego użytkownika !",
                                                 description=f"`{user.name} ma uprawnienia do wyrzucania !`",
                                                 color=disnake.Color.red(),
                                                 timestamp=disnake.utils.utcnow())

        authorkickfailure = disnake.Embed(title="️⚠️ Nie udało się wyrzucić tego użytkownika !",
                                          description="*Nie możesz wyrzucić samego siebie*",
                                          color=disnake.Color.red(),
                                          timestamp=disnake.utils.utcnow())

        if user != inter.author:
            if user.guild_permissions.kick_members:
                await inter.response.send_message(embed=mentioneduserkickfailure)
            else:
                await user.kick(reason=reason)
                await inter.response.send_message(embed=kicksuccess)
        else:
            await inter.response.send_message(embed=authorkickfailure)

    @kick.error
    async def kick_error(self, inter: disnake.ApplicationCommandInteraction, error):
        if isinstance(error, commands.MissingPermissions):
            missingpermsforkicking = disnake.Embed(title="⚠️ Brak permisji !",
                                                   description=f"`{error}`",
                                                   color=disnake.Color.red(),
                                                   timestamp=disnake.utils.utcnow())
            await inter.response.send_message(embed=missingpermsforkicking)

    @moderation.sub_command(name="unban", description="Odbanowywuje danego użytkownika !")
    async def unban(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User, reason: str = "."):
        successunban = disnake.Embed(title="✅ Sukces",
                                     description=f"Pomyślnie odbanowano {user.name}",
                                     color=disnake.Color.green(),
                                     timestamp=disnake.utils.utcnow())

        await inter.guild.unban(user, reason=reason)
        await inter.response.send_message(embed=successunban)

    @unban.error
    async def unban_error(self, inter: disnake.ApplicationCommandInteraction, error):
        if isinstance(error, commands.MissingPermissions):
            nopermsunban = disnake.Embed(title="⚠️ Błąd",
                                         description=f"'{error}'",
                                         color=disnake.Color.red(),
                                         timestamp=disnake.utils.utcnow())
            await inter.response.send_message(embed=nopermsunban)

    @moderation.sub_command(name="list", description="Lista zbanowanych użytkowników")
    async def banned_users(self, inter: disnake.ApplicationCommandInteraction):
        bans = await inter.guild.bans(limit=None).flatten()
        formatted_bans = [f"**Zbanowany użytkownik:** `{ban.user}` \n *Powód:* {ban.reason}" for ban in bans]
        output = "\n".join(formatted_bans)
        banned_users_list = disnake.Embed(title="🛠️ Lista zbanowanych użytkowników",
                                          description=f"{output}",
                                          color=disnake.Color.purple(),
                                          timestamp=disnake.utils.utcnow())
        await inter.response.send_message(embed=banned_users_list)

    @banned_users.error
    async def banned_users_error(self, inter, error):
        if isinstance(error, commands.MissingPermissions):
            missingbanlistperms = disnake.Embed(title="⚠️ Błąd permisji",
                                                description=f"`{error}`",
                                                color=disnake.Color.red(),
                                                timestamp=disnake.utils.utcnow())
            await inter.response.send_message(embed=missingbanlistperms)

    @moderation.sub_command(name="clear", description="Czyści podaną ilość wiadomości")
    async def clear(self, inter: disnake.ApplicationCommandInteraction, amount):
        successclearedmessages = disnake.Embed(title="✅ Sukces",
                                               description=f"Wyczyszczono `{amount}` wiad.",
                                               color=disnake.Color.green(),
                                               timestamp=disnake.utils.utcnow())

        await inter.channel.purge(limit=int(amount))
        await inter.response.send_message(embed=successclearedmessages)

    @clear.error
    async def clear_error(self, inter: disnake.ApplicationCommandInteraction, error):
        if isinstance(error, commands.MissingPermissions):
            missingclearperms = disnake.Embed(title="⚠️ Błąd permisji",
                                              description=f"`{error}`",
                                              color=disnake.Color.red(),
                                              timestamp=disnake.utils.utcnow())
            await inter.response.send_message(embed=missingclearperms)

    # Mute Command & Unmute using Discord's Built-In Timeout (gpt generated)

    @moderation.sub_command(name="mute", description="Wycisza użytkownika na określony czas.")
    async def mute(self, inter: disnake.ApplicationCommandInteraction, user: disnake.Member, time: str):
        mute_time_seconds = convert_time_to_seconds(time)
        if not mute_time_seconds:
            await inter.response.send_message("⚠️ Niepoprawny format czasu!", ephemeral=True)
            return

        mute_duration = timedelta(seconds=mute_time_seconds)

        try:
            await user.timeout(duration=mute_duration)
            usermutesuccesfully = disnake.Embed(title="✅ Sukces",
                                                description=f"✅ Użytkownik {user.mention} został wyciszony na {time}.")
            await inter.response.send_message(embed=usermutesuccesfully)
        except Exception as e:
            usermuteerror = disnake.Embed(title="⚠️ Błąd",
                                          description=f"Wystąpił błąd podczas wyciszania użytkownika: `{str(e)}`")
            await inter.response.send_message(embed=usermuteerror)

    @mute.error
    async def mute_error(self, inter: disnake.ApplicationCommandInteraction, error):
        if isinstance(error, commands.MissingPermissions):
            missingmuteperms = disnake.Embed(title="⚠️ Błąd permisji",
                                             description=f"`{error}`",
                                             color=disnake.Color.red(),
                                             timestamp=disnake.utils.utcnow())
            await inter.response.send_message(embed=missingmuteperms)

    @moderation.sub_command(name="unmute", description="Odcisza użytkownika.")
    async def unmute(self, inter: disnake.ApplicationCommandInteraction, user: disnake.Member):
        try:
            await user.timeout(duration=None)
            unmutedusersuccess = disnake.Embed(title="✅ Sukces",
                                               description=f"✅ Użytkownik {user.mention} został odciszony.")
            await inter.response.send_message(embed=unmutedusersuccess)
        except Exception as e:
            await inter.response.send_message(f"⚠️ Wystąpił nieoczekiwany błąd: {str(e)}", ephemeral=True)

    @unmute.error
    async def unmute_error(self, inter: disnake.ApplicationCommandInteraction, error):
        if isinstance(error, commands.MissingPermissions):
            missingmuteperms = disnake.Embed(title="⚠️ Błąd permisji",
                                             description=f"`{error}`",
                                             color=disnake.Color.red(),
                                             timestamp=disnake.utils.utcnow())
            await inter.response.send_message(embed=missingmuteperms)


def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))
