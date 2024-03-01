import disnake
from disnake.ext import commands
import datetime
def __init__(self, bot: commands.Bot):
    self.bot = bot
import disnake
from disnake.ext import commands
import datetime

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
    if time_seconds is None:
        return "0 sekund", "s"

    units = [
        ("tydzień", 604800),
        ("dzień", 86400),
        ("godzina", 3600),
        ("minuta", 60),
        ("sekunda", 1),
    ]
    result = []

    for unit_name, unit_duration in units:
        unit_count = time_seconds // unit_duration
        time_seconds %= unit_duration
        if unit_count > 0:
            if unit_name in ["sekunda", "minuta"]:
                plural_suffix = "y" if unit_count > 1 else ""
            else:
                plural_suffix = "y" if 5 > unit_count > 1 else ""  # Correct pluralization for other units
            result.append(f"{unit_count} {unit_name}{plural_suffix}")

    formatted_time = ", ".join(result)
    unit_text = "s" if time_seconds == 1 else ""  # Empty string for singular, "s" for plural

    return formatted_time if formatted_time else "0 sekund", unit_text


class Mute(commands.Cog):
    @commands.slash_command(name='mute', description='Wycisza daną osobę.', help='Dostępne jednostki: s, m, h, d')
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

        if time_seconds == 0:
            await inter.response.send_message("❌ Podano nieprawidłową liczbę czasu.", ephemeral=True)
            return

        end_time = datetime.datetime.now() + datetime.timedelta(seconds=time_seconds)
        await user.timeout(reason=reason, until=end_time)

        if user.id == inter.author.id:
            await inter.response.send_message("❌ Nie możesz wyciszyć siebie samego! :)", ephemeral=True)
            return

        formatted_time, unit_text = format_time(time_seconds)
        if time > 0:
            embed = disnake.Embed(
                description=f"✔ **{user.name}** został wyciszony przez **{inter.author}** na {formatted_time} {unit_text}, za {reason}",
                color=5420608
            )

            await inter.response.send_message(embed=embed)
        elif time < 0:
            embed = disnake.Embed(
                description="❌ Podano nieprawidłową liczbę czasu!",
                color=6881294
            )
            await inter.response.send_message(embed=embed)


class Unmute(commands.Cog):
    @commands.slash_command(description='Odcisza dana osobe.')
    async def unmute(self, inter, user: disnake.User):
        await user.timeout(duration=None)
        embed = disnake.Embed(
            description=f"✔ Odciszono uzytkownika **{user.name}**!",
            color=6881294
        )
        await inter.response.send_message(embed=embed)
class CheckMute(commands.Cog):
    @commands.slash_command(description='Sprawdza czy użytkownik jest wyciszony.')
    async def is_muted(self, inter, user: disnake.User):
        can_send_messages = inter.channel.permissions_for(user).send_messages
        if not can_send_messages:
            embed = disnake.Embed(
                description=f"✔ Użytkownik **{user.name}** jest wyciszony.",
                color=6881294
            )
            await inter.response.send_message(embed=embed)
        else:
            embed = disnake.Embed(
                description=f"❌ Użytkownik **{user.name}** nie jest wyciszony.",
                color=5420608
            )
            await inter.response.send_message(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Mute(bot))
    bot.add_cog(Unmute(bot))
    bot.add_cog(CheckMute(bot))