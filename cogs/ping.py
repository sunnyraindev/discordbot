import discord
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="ping", description="pong!")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")

    @commands.command(name="ping", help="Replies with Pong! (prefix)")
    async def prefix_ping(self, ctx: commands.Context):
        await ctx.send("Pong!")


async def setup(bot):
    await bot.add_cog(Ping(bot))