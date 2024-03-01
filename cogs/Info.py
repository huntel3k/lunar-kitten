import disnake
from disnake.ext import commands

class UserInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name='user', description='Podaje informacje o użytkowniku serwera.')
    async def UserInformation(self, inter, user: disnake.Member = None):
        user = user or inter.author
        avatar_url = user.avatar.url if user.avatar else user.default_avatar.url

        # Creating the download hyperlinks as text
        download_jpg_link = f"[.jpg]({avatar_url}.jpg)"
        download_png_link = f"[.png]({avatar_url}.png)"
        download_webp_link = f"[.webp]({avatar_url}.webp)"

        # Combining the download links as plain text
        download_links_text = f"{download_jpg_link} | {download_png_link} | {download_webp_link}"

        embed = disnake.Embed(
            title=f"🐱‍💻 Informacje o użytkowniku {user.name}",
            description=f"👥 ID użytkownika: {user.id}\n\n🔧 **Naciśnij wybrany przycisk aby pobrać zdjęcie profilowe z danym rozszerzeniem!**\n🌠 |{download_links_text}",
            color=6697881
        )

        embed.set_thumbnail(url=avatar_url)

        embed.add_field(name="⏰ Dołączono do serwera", value=user.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
        embed.set_footer(text=f"{inter.user.name} wykonał polecenie /user")
        await inter.response.send_message(embed=embed)

    @UserInformation.error
    async def userinformationerror(self, inter, error):
        if isinstance(error, disnake.ext.commands.errors.BadArgument):
            usernotfoundembed = disnake.Embed(
                title=f"⚠︎ Błąd!",
                description=f"Nie znaleziono wybranego użytkownika!",
                color=6697881
            )
            usernotfoundembed.set_footer(text=f"{inter.user.name} wykonał polecenie /user")
            await inter.response.send_message(embed=usernotfoundembed)

class ServerInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="serwer", description='Podaje informacje o serwerze.')
    async def ServerInformation(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
            title=f"🐱‍💻 Informacje o serwerze {inter.guild.name}",
            description=f"👥 Liczba członków: {inter.guild.member_count}",
            color=6697881
        )
        if inter.guild.icon:
            embed.set_thumbnail(url=inter.guild.icon.url)

        bans = await inter.guild.bans(limit=123).flatten()

        embed.add_field(name="🔨 Zbanowani użytkownicy:", value=len(bans), inline=True)
        embed.add_field(name="⏰ Data utworzenia:", value=inter.guild.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=True)
        embed.set_footer(text=f"{inter.user.name} wykonał polecenie /serwer")
        await inter.response.send_message(embed=embed)


class BotInfo(commands.Cog):
    @commands.slash_command(name="bot", description="Podaje informacje o bocie")
    async def BotInformation(inter):
        creator_id = 960970584123138158
        bot = inter.bot
        embed = disnake.Embed(
            title=f"🐱‍💻 Informacje o bocie {bot.user.name}",
            description=f"Twórca: <@{creator_id}>",
            color=6697881
        )
        embed.add_field(name="⏰ Data utworzenia bota:", value=inter.bot.user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        inline=True)
        embed.set_footer(text=f"{inter.user.name} wykonał polecenie /bot")
        await inter.response.send_message(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(UserInfo(bot))
    bot.add_cog(ServerInfo(bot))
    bot.add_cog(BotInfo(bot))