import discord
from discord.ext import commands, tasks
import asyncio

class MusicLoop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
        self.stream_url = "http://147.185.221.27:29891/brd"
        self.guild_id = 1241922816991825920
        self.channel_id = 1397617214986915870
        self.started = False

    @commands.Cog.listener()
    async def on_ready(self):
        if self.started:
            return
        self.started = True

        guild = self.bot.get_guild(self.guild_id)
        if not guild:
            print("Guild not found.")
            return

        channel = guild.get_channel(self.channel_id)
        if not channel:
            print("Voice channel not found.")
            return

        if not channel.permissions_for(guild.me).connect:
            print("Bot lacks permission to connect to voice.")
            return

        self.voice_client = await channel.connect()
        self.start_stream()

        self.ensure_playing_loop.start()  # Start background checker

    def start_stream(self):
        if self.voice_client and self.voice_client.is_connected():
            source = discord.FFmpegPCMAudio(self.stream_url)
            self.voice_client.play(
                source,
                after=lambda e: self.on_stream_end(e)
            )

    def on_stream_end(self, error):
        if error:
            print(f"[Stream Error] {error}")
        else:
            print("Stream ended. Restarting...")

        # Restart stream
        asyncio.run_coroutine_threadsafe(self.restart_stream(), self.bot.loop)

    async def restart_stream(self):
        await asyncio.sleep(1)  # Slight delay before reconnecting
        if self.voice_client and self.voice_client.is_connected():
            self.start_stream()

    @tasks.loop(seconds=30)
    async def ensure_playing_loop(self):
        """Checks periodically if the bot is still playing. If not, restarts the stream."""
        if (
            self.voice_client
            and self.voice_client.is_connected()
            and not self.voice_client.is_playing()
        ):
            print("[Checker] Bot is connected but not playing. Restarting stream...")
            self.start_stream()

    @ensure_playing_loop.before_loop
    async def before_checker(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(MusicLoop(bot))