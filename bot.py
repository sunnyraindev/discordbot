import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os

print("[Startup] Loading environment...")
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
print(f"[Startup] Token: {'Loaded' if TOKEN else 'Missing'}")

print("[Startup] Creating bot...")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="b!", intents=intents)

print("[Startup] Running bot...")
@bot.event
async def on_ready():
    await bot.tree.sync()  # Registers the slash commands
    print(f"Bot is ready. Logged in as {bot.user}")

@bot.event
async def setup_hook():
    for dirpath, dirnames, filenames in os.walk("./cogs"):
        for filename in filenames:
            if filename.endswith(".py") and not filename.startswith("_"):
                # Convert file path to dot notation
                relative_path = os.path.relpath(os.path.join(dirpath, filename), "./cogs")
                module = "cogs." + relative_path.replace(os.sep, ".")[:-3]  # strip ".py"
                try:
                    await bot.load_extension(module)
                    print(f"✅ Loaded {module}")
                except Exception as e:
                    print(f"❌ Failed to load {module}: {e}")


bot.run(TOKEN)