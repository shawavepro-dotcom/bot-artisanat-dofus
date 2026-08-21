import discord
from discord import app_commands
from discord.ext import commands

class Supprimer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="supprimer", description="Supprime un métier de votre profil artisan.")
    @app_commands.describe(metier="Le métier que vous souhaitez retirer de votre profil.")
    async def supprimer(self, interaction: discord.Interaction, metier: str):
        user_id = interaction.user.id

        async with self.bot.db.pool.acquire() as conn:
            result = await conn.execute(
                "DELETE FROM artisans WHERE user_id = $1 AND metier = $2",
                user_id, metier.lower()
            )

        await interaction.response.send_message(
            f"🗑️ Le métier **{metier}** a été supprimé de votre profil.",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Supprimer(bot))
