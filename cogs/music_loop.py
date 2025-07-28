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
        if not self.started:
            self.started = True
            self.bot.loop.create_task(self.safe_start())

    async def safe_start(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(5)  # Ensure all shards and caches are ready
        await self.connect_and_play()
        self.ensure_alive.start()


    async def connect_and_play(self):
        guild = self.bot.get_guild(self.guild_id)
        if not guild:
            print("Guild not found.")
            return

        channel = guild.get_channel(self.channel_id)
        if not channel:
            print("Voice channel not found.")
            return

        if not self.voice_client:
            self.voice_client = channel.guild.voice_client

        if not self.voice_client or not self.voice_client.is_connected():
            self.voice_client = await channel.connect(reconnect=True)

            self.start_stream()

    def start_stream(self):
        if self.voice_client and self.voice_client.is_connected():
            if not self.voice_client.is_playing():
                source = discord.FFmpegPCMAudio(self.stream_url)
                self.voice_client.play(source, after=lambda e: self.on_stream_end(e))
                print("Started stream.")
            else:
                print("Stream is already playing.")
        else:
            print("Cannot start stream: not connected.")

    def on_stream_end(self, error):
        if error:
            print(f"Stream error: {error}")
        else:
            print("Stream ended.")

        async def safe_restart():
            await asyncio.sleep(2)
            try:
                await self.restart()
            except Exception as e:
                print(f"Restart failed: {e}")

        asyncio.run_coroutine_threadsafe(safe_restart(), self.bot.loop)

    async def restart(self):
        print("Restarting stream...")
        await asyncio.sleep(1)
        if self.voice_client and not self.voice_client.is_connected():
            await self.connect_and_play()
        else:
            self.start_stream()

    @tasks.loop(seconds=30)
    async def ensure_alive(self):
        if not self.voice_client or not self.voice_client.is_connected():
            print("[Check] Voice client disconnected. Reconnecting...")
            await self.connect_and_play()
        elif not self.voice_client.is_playing():
            print("[Check] Voice connected but not playing. Restarting stream...")
            self.start_stream()

    @ensure_alive.before_loop
    async def before_ensure_alive(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(MusicLoop(bot))