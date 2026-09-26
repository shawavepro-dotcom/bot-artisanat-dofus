import discord
from discord import app_commands
from discord.ext import commands
import traceback
from commands.metiers import METIERS

class Referencer(commands.Cog):
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

    @app_commands.command(name="referencer", description="Ajoute un métier à un profil artisan.")
    @app_commands.describe(
        metier="Le métier à ajouter",
        niveau="Le niveau dans ce métier",
        utilisateur="L'utilisateur à référencer (optionnel - vous par défaut)"
    )
    @app_commands.autocomplete(metier=metier_autocomplete)
    async def referencer(self, interaction: discord.Interaction, metier: str, niveau: int, utilisateur: discord.User = None):
        try:
            metier_lower = metier.lower()
            
            # Validation: le métier doit être dans la liste
            if metier_lower not in METIERS:
                await interaction.response.send_message(
                    f"❌ Oups, ce métier n'est pas disponible sur Dofus. Peux être devrait tu donner l'idée à Ankama ? :D",
                    ephemeral=True
                )
                return
            
            # Si aucun utilisateur n'est spécifié, utiliser l'utilisateur qui a lancé la commande
            target_user = utilisateur if utilisateur else interaction.user
            user_id = str(target_user.id)

            async with self.bot.db.pool.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO artisans (user_id, metier, niveau)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (user_id, metier)
                    DO UPDATE SET niveau = EXCLUDED.niveau
                    """,
                    user_id, metier_lower, niveau
                )

            await interaction.response.send_message(
                f"✅ Métier **{metier.capitalize()}** enregistré avec le niveau **{niveau}** pour {target_user.mention}.",
                ephemeral=True
            )
        except Exception as e:
            print(f"❌ Erreur dans /referencer : {e}")
            traceback.print_exc()
            try:
                await interaction.response.send_message(
                    f"❌ Erreur : {str(e)}",
                    ephemeral=True
                )
            except:
                pass

async def setup(bot):
    await bot.add_cog(Referencer(bot))

