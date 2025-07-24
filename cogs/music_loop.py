import discord
from discord.ext import commands
import os
import asyncio
import random

class MusicLoop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
        self.stream_url = "http://147.185.221.27:29891/braxii"
        self.guild_id = 1241922816991825920
        self.channel_id = 1397617214986915870
        self.started = False

    @commands.Cog.listener()
    async def on_ready(self):
        if self.voice_client and self.voice_client.is_connected():
            return

        guild = self.bot.get_guild(self.guild_id)
        channel = guild.get_channel(self.channel_id)
        if not channel:
            print("Voice channel not found.")
            return

        self.voice_client = await channel.connect()
        source = discord.FFmpegPCMAudio(self.stream_url)
        self.voice_client.play(source, after=lambda e: print(f"Player error: {e}" if e else "Stream ended."))

            

async def setup(bot):
    await bot.add_cog(MusicLoop(bot))