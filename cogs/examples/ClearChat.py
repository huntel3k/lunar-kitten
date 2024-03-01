import disnake
from disnake.ext import commands


class ClearChat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def check_permissions(self, inter):
        # Check if the user has the 'manage_messages' permission
        return inter.author.guild_permissions.manage_messages

    @commands.slash_command(description='Czysci podana ilosc wiadomosci.')
    async def clear(self, inter, amount: int):
        try:
            if await self.check_permissions(inter):
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
                print("❌ An error occurred: Unable to defer the response and send a new message.")
        except Exception as e:
            print(f"❌ An error occurred: {e}")


def setup(bot: commands.Bot):
    bot.add_cog(ClearChat(bot))
