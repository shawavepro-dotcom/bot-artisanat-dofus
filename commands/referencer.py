import discord
from discord import app_commands
from discord.ext import commands

class Referencer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="referencer",
        description="Référencer ton métier d'artisan."
    )
    @app_commands.describe(
        metier="Ton métier (ex: tailleur, cordonnier, bijoutier)",
        niveau="Ton niveau (1 à 200)"
    )
    async def referencer(self, interaction: discord.Interaction, metier: str, niveau: int):

        # Vérification du niveau
        if niveau < 1 or niveau > 200:
            await interaction.response.send_message(
                "❌ Le niveau doit être entre **1 et 200**.",
                ephemeral=True
            )
            return

        user_id = str(interaction.user.id)

        # Insertion dans la base
        async with self.bot.db.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO artisans (user_id, metier, niveau)
                VALUES ($1, $2, $3)
                ON CONFLICT (user_id, metier)
                DO UPDATE SET niveau = EXCLUDED.niveau;
            """, user_id, metier.lower(), niveau)

        await interaction.response.send_message(
            f"✅ Tu es maintenant référencé comme **{metier.capitalize()} niveau {niveau}** !",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Referencer(bot))
