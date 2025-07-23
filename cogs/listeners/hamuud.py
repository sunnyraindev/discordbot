import discord
from discord.ext import commands

class Hamuud(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
    
        if message.content.startswith('hamuud'):
            await message.channel.send(file=discord.File(r'c:\Users\roro\Downloads\bot\videos\hamood.mp4'))


async def setup(bot):
    await bot.add_cog(Hamuud(bot))