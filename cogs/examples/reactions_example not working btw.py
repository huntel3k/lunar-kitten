from disnake.ext import commands


class Reaction(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name='add_reaction', description='Add an emoji reaction to an existing message')
    async def add_reaction_to_message(self, inter, message_id: str, emoji: str):
        try:
            # Fetch the message by its ID
            message = await inter.channel.fetch_message(int(message_id))
        except Exception as e:
            print(f"Error fetching message: {e}")
            return

        if message is None:
            print("Error: Message not found")
            return

        try:
            # Add the reaction to the message
            await message.add_reaction(emoji)
            await inter.response.send_message("Reaction added successfully!")
        except Exception as e:
            print(f"Error adding reaction: {e}")
            await inter.response.send_message("Failed to add reaction")


def setup(bot: commands.Bot):
    bot.add_cog(Reaction(bot))
