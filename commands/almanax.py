import discord
from discord import app_commands
from discord.ext import commands, tasks
import json
import os
from datetime import datetime
import pytz
import traceback

# Configuration
SALON_ID = 1534855459415261185  # ID du salon pour publier
EMBED_COLOR = discord.Color.gold()
OWNER_ID = 1400924331479142511  # ID Discord de Biafina

class Almanax(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_published_month = None  # Track du dernier mois publié
        self.publication_loop.start()

    def cog_unload(self):
        self.publication_loop.cancel()

    def load_almanax_data(self):
        """Charge les données du JSON"""
        try:
            with open("data/almanax_monthly.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Erreur lors du chargement du JSON Almanax : {e}")
            return {}

    def get_current_month_fr(self):
        """Retourne le nom du mois en français"""
        months_fr = {
            1: "janvier", 2: "février", 3: "mars", 4: "avril",
            5: "mai", 6: "juin", 7: "juillet", 8: "août",
            9: "septembre", 10: "octobre", 11: "novembre", 12: "décembre"
        }
        return months_fr.get(datetime.now().month, "")

    def create_embed(self, month_name):
        """Crée l'embed Discord avec les données du JSON"""
        data = self.load_almanax_data()
        
        if month_name.lower() not in data:
            return None
        
        month_data = data[month_name.lower()]
        
        embed = discord.Embed(
            title=month_data.get("title", f"Bonus Almanax du mois"),
            description=month_data.get("content", ""),
            color=EMBED_COLOR
        )
        
        embed.set_footer(text="Bot Artisanat Dofus | Mis à jour automatiquement")
        
        return embed

    @tasks.loop(minutes=1)
    async def publication_loop(self):
        """Boucle qui vérifie chaque minute si c'est le moment de publier"""
        try:
            # Timezone France (UTC+2 en été, UTC+1 en hiver)
            tz_fr = pytz.timezone('Europe/Paris')
            now_fr = datetime.now(tz_fr)
            
            # Vérifier si c'est le 1er du mois à 18:00
            # ET qu'on n'a pas déjà publié ce mois
            current_month = now_fr.month
            
            if (now_fr.day == 1 and now_fr.hour == 18 and now_fr.minute == 0 
                and self.last_published_month != current_month):
                await self.publish_monthly_almanax()
                self.last_published_month = current_month  # Marquer comme publié
        except Exception as e:
            print(f"❌ Erreur dans publication_loop : {e}")
            traceback.print_exc()

    @publication_loop.before_loop
    async def before_publication_loop(self):
        """Attend que le bot soit prêt avant de démarrer la boucle"""
        await self.bot.wait_until_ready()

    async def publish_monthly_almanax(self):
        """Publie le message mensuel d'Almanax"""
        try:
            month_name = self.get_current_month_fr()
            
            if not month_name:
                print("❌ Impossible de déterminer le mois")
                return
            
            embed = self.create_embed(month_name)
            
            if not embed:
                print(f"❌ Pas de données pour le mois : {month_name}")
                return
            
            # Récupérer le salon
            salon = self.bot.get_channel(SALON_ID)
            if not salon:
                print(f"❌ Salon {SALON_ID} non trouvé")
                return
            
            # Publier le message
            await salon.send(embed=embed)
            print(f"✅ Message Almanax publié pour {month_name.capitalize()}")
        
        except Exception as e:
            print(f"❌ Erreur lors de la publication Almanax : {e}")
            traceback.print_exc()

    @app_commands.command(
        name="test-almanax",
        description="Teste l'affichage du bonus Almanax du mois en cours (Biafina only)"
    )
    async def test_almanax(self, interaction: discord.Interaction):
        """Commande de test pour voir le rendu avant la vraie publication"""
        # Vérifier que c'est Biafina
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message(
                "❌ Cette commande est réservée à Biafina!",
                ephemeral=True
            )
            return
        
        try:
            month_name = self.get_current_month_fr()
            embed = self.create_embed(month_name)
            
            if not embed:
                await interaction.response.send_message(
                    f"❌ Pas de données pour le mois : {month_name}",
                    ephemeral=True
                )
                return
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            print(f"✅ Test Almanax pour {month_name} réussi")
        
        except Exception as e:
            print(f"❌ Erreur dans /test-almanax : {e}")
            traceback.print_exc()
            await interaction.response.send_message(
                f"❌ Erreur : {str(e)}",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Almanax(bot))

