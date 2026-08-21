import os
import discord
from discord.ext import commands
from database import Database
import asyncio

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# On attache la base au bot
bot.db = Database()

@bot.event
async def on_ready():
    await bot.db.connect()
    await bot.tree.sync()
    print(f"Bot connecté : {bot.user}")

async def load_commands():
    # Charge automatiquement tous les fichiers .py du dossier /commands
    for file in os.listdir("./commands"):
        if file.endswith(".py"):
            await bot.load_extension(f"commands.{file[:-3]}")

async def main():
    await load_commands()
    await bot.start(os.getenv("TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
