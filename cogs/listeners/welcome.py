from collections import UserList
import discord
from discord.ext import commands
import json
import os


DATA_FILE = "data.json"


def load_joined_users():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_joined_users(user_list):
    with open(DATA_FILE, "w") as f:
        json.dump(user_list, f)


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.joined_users = load_joined_users()

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = discord.utils.get(member.guild.text_channels, name="welcome-bye")
        if not channel:
            return

        human_role = discord.utils.get(member.guild.roles, id=1241926830139637871)
        bot_role = discord.utils.get(member.guild.roles, id=1265420082473861162)
        if member and human_role:
            await member.add_roles(human_role)
        if member.bot and bot_role:
            await member.add_roles(bot_role)

        # Check if user joined before
        if member.id in self.joined_users:
            await channel.send(f"➡️ {member.mention} joined the server! Please don't leave again 🥺")
        else:
            self.joined_users.append(member.id)
            save_joined_users(self.joined_users)
            await channel.send(f"➡️ {member.mention} joined the server!")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        channel = discord.utils.get(member.guild.text_channels, name="welcome-bye")
        if channel:
            await channel.send(f"⬅️ {member.mention} left the server")

async def setup(bot):
    await bot.add_cog(Welcome(bot))