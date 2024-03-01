import disnake
from disnake.ext import commands

bot = commands.Bot(command_prefix='/')

class Test(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @commands.slash_command(name='moderate', description='Moderation commands')
    async def moderate(ctx):
        await ctx.send('Choose a moderation action.')

    @moderate.sub_command(name='ban', description='Ban a user')
    async def ban(ctx):
        await ctx.send('Banning user.')

    @moderate.sub_command(name='kick', description='Kick a user')
    async def kick(ctx):
        await ctx.send('Kicking user.')

def setup(bot: commands.Bot):
    bot.add_cog(Test(bot))