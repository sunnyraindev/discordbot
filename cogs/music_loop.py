import discord
from discord.ext import commands
import os
import asyncio
import random

class MusicLoop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
        self.song_dir = os.path.join(os.path.dirname(__file__), '..', 'songs')
        self.guild_id = 1241922816991825920
        self.channel_id = 1397617214986915870
        self.started = False

    @commands.Cog.listener()
    async def on_ready(self):
        if self.started:
            return  # Don't run again on reconnect
        self.started = True
        await self.join_and_loop()
    
    async def join_and_loop(self):
        try:
            guild = self.bot.get_guild(self.guild_id)
            if guild is None:
                print("[Music] Guild not found.")
                return
        
            channel = guild.get_channel(self.channel_id)
            if channel is None:
                print("[Music] Voice channel not found.")
                return

            self.voice_client = await channel.connect()
            print("[Music] Connected to voice channel.")
            self.bot.loop.create_task(self.play_loop())
        except Exception as e:
            print(f"[Music] ERROR in join_and_loop: {e}")

    async def play_loop(self):
        while True:
            if not self.voice_client or not self.voice_client.is_connected():
                print("[Music] Voice client disconnected. Stopping loop.")
                break  # Exit loop if disconnected (or reconnect logic can be added)

            songs = [f for f in os.listdir(self.song_dir) if f.endswith(".mp3")]
            if not songs:
                print("[Music] No songs found. Sleeping...")
                await asyncio.sleep(10)
                continue

            random.shuffle(songs)

            for song in songs:
                if not self.voice_client or not self.voice_client.is_connected():
                    print("[Music] Voice client disconnected during playback.")
                    return

                song_path = os.path.join(self.song_dir, song)
                audio = discord.FFmpegPCMAudio(song_path)

                # Ensure previous song isn't playing
                while self.voice_client.is_playing():
                    print("[Music] Waiting for current song to finish...")
                    await asyncio.sleep(1)

                # Play song
                self.voice_client.play(audio)
                print(f"[Music] Now playing: {song}")

                # Wait for this song to finish
                while self.voice_client.is_playing():
                    await asyncio.sleep(1)

            # Optional: small pause between loops
            await asyncio.sleep(2)
            

async def setup(bot):
    await bot.add_cog(MusicLoop(bot))