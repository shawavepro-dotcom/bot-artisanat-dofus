import discord
from discord import app_commands
from discord.ext import commands
import traceback
from commands.metiers import METIERS

class Supprimer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def metier_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        """Autocomplétion pour les métiers disponibles"""
        choices = [m for m in METIERS if m.startswith(current.lower())]
        return [app_commands.Choice(name=m.capitalize(), value=m) for m in choices[:25]]

    @app_commands.command(name="supprimer", description="Supprime un métier de votre profil artisan.")
    @app_commands.describe(metier="Le métier que vous souhaitez retirer de votre profil.")
    @app_commands.autocomplete(metier=metier_autocomplete)
    async def supprimer(self, interaction: discord.Interaction, metier: str):
        try:
            metier_lower = metier.lower()
            
            # Validation: le métier doit être dans la liste
            if metier_lower not in METIERS:
                await interaction.response.send_message(
                    f"❌ Oups, ce métier n'est pas disponible sur Dofus. Peux être devrait tu donner l'idée à Ankama ? :D",
                    ephemeral=True
                )
                return
            
            user_id = str(interaction.user.id)

            async with self.bot.db.pool.acquire() as conn:
                result = await conn.execute(
                    "DELETE FROM artisans WHERE user_id = $1 AND metier = $2",
                    user_id, metier_lower
                )

            await interaction.response.send_message(
                f"🗑️ Le métier **{metier.capitalize()}** a été supprimé de votre profil.",
                ephemeral=True
            )
        except Exception as e:
            print(f"❌ Erreur dans /supprimer : {e}")
            traceback.print_exc()
            try:
                await interaction.response.send_message(
                    f"❌ Erreur : {str(e)}",
                    ephemeral=True
                )
            except:
                pass

async def setup(bot):
    await bot.add_cog(Supprimer(bot))

