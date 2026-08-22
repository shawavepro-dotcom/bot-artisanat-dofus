import discord
from discord import app_commands
from discord.ext import commands

class Referencer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="referencer", description="Ajoute un métier à votre profil artisan.")
    @app_commands.describe(metier="Le métier à ajouter", niveau="Votre niveau dans ce métier")
    async def referencer(self, interaction: discord.Interaction, metier: str, niveau: int):
        user_id = interaction.user.id

        async with self.bot.db.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO artisans (user_id, metier, niveau)
                VALUES ($1, $2, $3)
                ON CONFLICT (user_id, metier)
                DO UPDATE SET niveau = EXCLUDED.niveau
                """,
                user_id, metier.lower(), niveau
            )

        await interaction.response.send_message(
            f"✅ Métier **{metier}** enregistré avec le niveau **{niveau}**.",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Referencer(bot))
