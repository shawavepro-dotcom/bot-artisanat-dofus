import os
import discord
from discord.ext import commands
from database import Database

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
db = Database()

@bot.event
async def on_ready():
    await db.connect()
    print(f"Bot connecté : {bot.user}")

bot.run(os.getenv("TOKEN"))
