import discord
import armazenamento
#import requests
from discord import app_commands
from discord.ext import commands

class Conexoes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name = "conectar_repositorio", description = "conecta um repositório a um canal")
    @app_commands.describe(criador = "criador do repositório", repositorio = "nome do repositório")
    async def conectar(self, interaction: discord.Interaction, criador:str, repositorio: str):
        nome = f"{criador}/{repositorio}".lower()

        # pega o id do canal, e faz a modificação dentro do arquivo conect.json
        # o primeiro bglh do dicionario é o dono do repositorio e o repositorio dele
        # o segundo é o id do canal do discord
        conexoes = armazenamento.carregar()
        conexoes[nome] = interaction.channel_id
        armazenamento.salvar(conexoes)

        await interaction.response.send_message(f"O repositório {nome} foi conectado neste canal.", ephemeral=True)

async def setup(bot):
   await bot.add_cog(Conexoes(bot))