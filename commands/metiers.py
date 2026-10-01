import discord
from discord import app_commands
from discord.ext import commands
import traceback

METIERS = [
    "alchimiste", "bijoutier", "bricoleur",
    "bûcheron", "chasseur", "cordomage", "cordonnier", "costumage",
    "eleveur", "façomage", "façonneur", "forgeron", "forgemage", "joaillomage", "mineur",
    "paysan", "pêcheur", "sculptemage", "sculpteur",
    "tailleur"
]

class Metiers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="metiers", description="Affiche la liste des métiers disponibles avec le nombre d'artisans.")
    async def metiers(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(
                title="Liste des métiers disponibles",
                color=discord.Color.green()
            )

            async with self.bot.db.pool.acquire() as conn:
                for m in METIERS:
                    # Compter le nombre d'artisans pour ce métier
                    count = await conn.fetchval(
                        "SELECT COUNT(*) FROM artisans WHERE metier = $1",
                        m
                    )
                    
                    # Afficher "artisan" ou "artisans" selon le nombre
                    artisan_text = "artisan" if count == 1 else "artisans"
                    embed.add_field(
                        name=m.capitalize(),
                        value=f"{count} {artisan_text}",
                        inline=True
                    )

            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            print(f"❌ Erreur dans /metiers : {e}")
            traceback.print_exc()
            try:
                await interaction.response.send_message(
                    f"❌ Erreur : {str(e)}",
                    ephemeral=True
                )
            except:
                pass

async def setup(bot):
    await bot.add_cog(Metiers(bot))

