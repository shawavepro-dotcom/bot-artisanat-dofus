import os
import discord
from discord.ext import commands
from database import Database
from init_db import init_database
import asyncio

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# On attache la base au bot
bot.db = Database()

@bot.event
async def on_ready():
    print(f"Bot connecté : {bot.user}")
    try:
        await bot.db.connect()
        print("✅ Connexion à la base de données établie")
        await init_database()
        print("✅ Initialisation de la base de données complétée")
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} commandes slash synchronisées")
    except Exception as e:
        print(f"❌ Erreur dans on_ready : {e}")
        import traceback
        traceback.print_exc()

async def load_commands():
    # Charge automatiquement tous les fichiers .py du dossier /commands
    print("📂 Chargement des commandes...")
    for file in os.listdir("./commands"):
        if file.endswith(".py"):
            try:
                await bot.load_extension(f"commands.{file[:-3]}")
                print(f"  ✅ {file} chargé")
            except Exception as e:
                print(f"  ❌ Erreur lors du chargement de {file} : {e}")
                import traceback
                traceback.print_exc()

async def main():
    print("🚀 Démarrage du bot...")
    await load_commands()
    await bot.start(os.getenv("TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())

