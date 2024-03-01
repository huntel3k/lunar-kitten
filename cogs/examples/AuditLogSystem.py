from disnake.ext import commands


class AuditLogChannelSetup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.observed_channel_ids = [1208460319316377640]  # Lista identyfikatorów kanałów do obserwacji

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready!")
        print("Guilds bot is in:")
        for guild in self.bot.guilds:
            print(guild.name)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        print(f"Zdarzenie on_guild_channel_create zostało wyzwalone dla kanału {channel.name} (ID: {channel.id}).")

        # Sprawdź, czy to kanał, który obserwujemy
        if channel.id in self.observed_channel_ids:
            print("Nowy kanał został utworzony i odpowiada obserwowanemu kanałowi.")

            # Wyślij powiadomienie na innym kanale
            notification_channel = channel.guild.get_channel(channel.id)
            if notification_channel:
                print("Znaleziono kanał powiadomień.")
                await notification_channel.send(f"Nowy kanał {channel.name} został utworzony!")
            else:
                print("Nie można znaleźć kanału powiadomień.")
        else:
            print("Zdarzenie dotyczy kanału, który nie jest obserwowany.")
            print(f"Lista obserwowanych kanałów: {self.observed_channel_ids}")
            print(f"Zdarzenie wyzwalane na serwerze: {channel.guild.name}")


def setup(bot: commands.Bot):
    bot.add_cog(AuditLogChannelSetup(bot))
