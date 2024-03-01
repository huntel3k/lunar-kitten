import discord
from discord.ext import commands
import json

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.level_data = {}

        # Load level data from a file
        try:
            with open("level_data.json", "r") as file:
                self.level_data = json.load(file)
        except FileNotFoundError:
            pass

    def save_data(self):
        # Save level data to a file
        with open("level_data.json", "w") as file:
            json.dump(self.level_data, file)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Add XP for each message
        user_id = str(message.author.id)
        self.level_data.setdefault(user_id, {"xp": 0, "level": 1})
        self.level_data[user_id]["xp"] += 10  # You can adjust the XP gained per message

        # Check for level up
        if self.level_data[user_id]["xp"] >= self.calculate_xp_required(self.level_data[user_id]["level"]):
            self.level_data[user_id]["xp"] = 0
            self.level_data[user_id]["level"] += 1
            await message.channel.send(f"{message.author.mention} has leveled up to level {self.level_data[user_id]['level']}!")

        # Save data after each message
        self.save_data()

    def calculate_xp_required(self, level):
        # You can customize the XP required for each level as per your preference
        return 100 + (level - 1) * 50

    @commands.command(name="level")
    async def get_level(self, ctx, user: discord.User = None):
        user = user or ctx.author
        user_id = str(user.id)
        level_data = self.level_data.get(user_id, {"xp": 0, "level": 1})
        await ctx.send(f"{user.mention} is at level {level_data['level']} with {level_data['xp']} XP.")

def setup(bot):
    bot.add_cog(Leveling(bot))
