import discord
from discord import app_commands
from discord.ext import commands

class Recherche(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="recherche", description="Recherche les artisans d'un métier.")
    @app_commands.describe(metier="Le métier recherché")
    async def recherche(self, interaction: discord.Interaction, metier: str):
        async with self.bot.db.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT user_id, niveau FROM artisans WHERE metier = $1 ORDER BY niveau DESC",
                metier.lower()
            )

        if not rows:
            await interaction.response.send_message(
                f"❌ Aucun artisan trouvé pour le métier **{metier}**.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title=f"Artisans trouvés : {metier.capitalize()}",
            color=discord.Color.orange()
        )

        for row in rows:
            user = interaction.guild.get_member(row["user_id"])
            nom = user.display_name if user else f"Utilisateur {row['user_id']}"
            embed.add_field(
                name=nom,
                value=f"Niveau {row['niveau']}",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Recherche(bot))
