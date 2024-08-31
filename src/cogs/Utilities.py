import random

import disnake
from disnake.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="fun")
    async def fun(self, inter):
        pass

    @fun.sub_command(name="cats", description="Pokazuje losowe zdjecia kotow!")
    async def cat(self, inter):
        catgifs = ["https://media.tenor.com/QUSMUwP4DX4AAAAi/plink-cat-blink.gif",
                   "https://media1.tenor.com/m/_t0sHU9OPmsAAAAC/-.gif",
                   "https://media1.tenor.com/m/MFt1WVDeUhUAAAAd/smol-illegally-smol-cat.gif",
                   "https://media1.tenor.com/m/nisaHYy8yAYAAAAd/besito-catlove.gif",
                   "https://media.tenor.com/Mow3BwJQLc8AAAAi/cat-cat-meme.gif",
                   "https://media.tenor.com/19B3eSbZ7CkAAAAi/verycat-cat-eating-chips.gif",
                   "https://media.tenor.com/kWlwZ9Hy6TAAAAAi/peach-goma-goma.gif"
                   ]

        catgif = random.choice(catgifs)
        catgenerator = disnake.Embed(title="meow !",
                                     color=disnake.Color.random())
        catgenerator.set_image(url=catgif)
        await inter.send(embed=catgenerator)


class Tools(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="about")
    async def about(self, inter):
        pass

    @about.sub_command(name="bot", description="Informacje o bocie!")
    async def bot(self, inter: disnake.ApplicationCommandInteraction):
        aboutbot = disnake.Embed(title=f"🛠️ -| @lunar kitten |- 🛠️",
                                 description=f"🏓 Ping bota wynosi: `{round(self.bot.latency * 1000)} ms` ⏱️",
                                 color=disnake.Color.dark_blue(),
                                 timestamp=disnake.utils.utcnow())
        aboutbot.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/1194562644905050133/bc9190c57fdef38ed690c16fa9d0384e.png?size=1024")
        await inter.response.send_message(embed=aboutbot)

    @about.sub_command(name="user", description="Pokazuje informacje o danym użytkowniku !")
    async def user(self, inter, user: disnake.Member):
        aboutuser = disnake.Embed(title=f"Informacje o @{user.name}",
                                  color=disnake.Color.dark_blue(),
                                  timestamp=disnake.utils.utcnow())

        timestamp_created = int(user.created_at.timestamp())
        formatted_time_created = f"<t:{timestamp_created}:F>"

        timestamp_joined = int(user.joined_at.timestamp())
        formatted_time_joined = f"<t:{timestamp_joined}:F>"

        roles = [role.mention for role in user.roles]
        formatted_roles = "\n".join(roles)

        activity = user.activity  # Get the user's current activity

        if activity is not None:
            activity_type = activity.type.name.capitalize()  # Get the activity type as a string and capitalize it
            activity_name = activity.name  # Get the name of the activity
            formatted_activity = f"{activity_type}: *{activity_name}*"  # Format it nicely
        else:
            formatted_activity = "Użytkownik nic nie robi"

        status = user.status

        aboutuser.set_thumbnail(url=user.avatar.url)
        aboutuser.description = f"[Pobierz zdjęcie profilowe]({user.avatar.url})"
        aboutuser.add_field(name="Data utworzenia konta:", value=formatted_time_created, inline=True)
        aboutuser.add_field(name="Data dołączenia:", value=formatted_time_joined, inline=False)
        aboutuser.add_field(name="Role użytkownika:", value=formatted_roles, inline=False)
        aboutuser.add_field(name="Status: ", value=status, inline=True)
        aboutuser.add_field(name="Co robi w tym momencie: ", value=formatted_activity, inline=True)
        aboutuser.set_footer(text=f"ID: {user.id}")
        await inter.response.send_message(embed=aboutuser)

    @about.sub_command(name="server", description="Wyświetla informacje o serwerze !")
    async def server(self, inter):

        timestamp_created = int(inter.guild.created_at.timestamp())
        formatted_time_created = f"<t:{timestamp_created}:F>"

        aboutserver = disnake.Embed(description=f"Informacje o serwerze {inter.guild.name}",
                                    color=disnake.Color.dark_blue(),
                                    timestamp=disnake.utils.utcnow())
        aboutserver.set_thumbnail(url=inter.guild.icon.url)
        aboutserver.add_field(name="Data utworzenia: ", value=formatted_time_created, inline=False)
        aboutserver.add_field(name="Utworzony przez ", value=inter.guild.owner.mention, inline=True)
        aboutserver.add_field(name="Liczba członków: ", value=inter.guild.member_count, inline=True)
        aboutserver.add_field(name="Poziom weryfikacji: ", value=inter.guild.verification_level, inline=False)

        await inter.response.send_message(embed=aboutserver)


def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))
    bot.add_cog(Tools(bot))
