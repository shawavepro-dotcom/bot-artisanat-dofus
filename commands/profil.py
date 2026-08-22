import discord
from discord import app_commands
from discord.ext import commands

class Profil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="profil", description="Affiche votre profil artisan.")
    @app_commands.describe(membre="Le membre dont vous voulez voir le profil.")
    async def profil(self, interaction: discord.Interaction, membre: discord.Member = None):
        cible = membre or interaction.user
        user_id = cible.id

        async with self.bot.db.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT metier, niveau FROM artisans WHERE user_id = $1",
                user_id
            )

        if not rows:
            await interaction.response.send_message(
                f"❌ {cible.display_name} n'a aucun métier référencé.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title=f"Profil artisan : {cible.display_name}",
            color=discord.Color.blue()
        )

        for row in rows:
            embed.add_field(
                name=row["metier"].capitalize(),
                value=f"Niveau {row['niveau']}",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Profil(bot))