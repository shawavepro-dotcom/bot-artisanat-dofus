import discord
from discord import app_commands
from discord.ext import commands

METIERS = [
    "alchimiste", "bijoutier", "boucher", "boulanger", "bricoleur",
    "bûcheron", "chasseur", "cordomage", "cordonnier", "costumage",
    "façomage", "forgeron", "forgemage", "joaillomage", "mineur",
    "paysan", "pêcheur", "poisonnier", "sculptemage", "sculpteur",
    "tailleur"
]

class Metiers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="metiers", description="Affiche la liste des métiers disponibles.")
    async def metiers(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Liste des métiers disponibles",
            color=discord.Color.green()
        )

        for m in METIERS:
            embed.add_field(name=m.capitalize(), value="Disponible", inline=True)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Metiers(bot))