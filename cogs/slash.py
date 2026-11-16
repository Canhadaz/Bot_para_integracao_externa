import discord
import apigithub
import requests
from discord import app_commands
from discord.ext import commands

# os comandos do but
class SlashComandos(commands.Cog):
   def __init__(self, bot):
    self.bot = bot

   @app_commands.command(name="ping", description="Responde com a latência do bot via Slash Command.")
   async def ping(self, interaction: discord.Interaction):
      latencia = round(self.bot.latency * 1000)
      
      await interaction.response.send_message(f"Pong! ({latencia}ms)")

   @app_commands.command(name="dizer", description="Faz o bot repetir o que você digitar.")
   @app_commands.describe(texto="O que você quer que o bot diga?")
   async def dizer(self, interaction: discord.Interaction, texto: str):
      await interaction.response.send_message(f"Você disse: {texto}")

   @app_commands.command(name="consultar_usuario", description="Consulta a usuário cadastrado no github")
   async def painel(self, interaction: discord.Interaction, usuario: str):
      await interaction.response.defer(ephemeral = True) # a resposta só fica visivel pra quem usou o comando
      
      try:
         api = apigithub.Api_github(usuario)
         resposta = api.requisicao_usuario()

         if not isinstance(resposta, dict):
            await interaction.followup.send(
                  f"Usuário: {usuario} não encontrado! (Status: {resposta}).", 
                  ephemeral=True
            )
            return

         embed = discord.Embed(
            title=f"Perfil de: {resposta.get('login', usuario)}",
            url=resposta.get('html_url', ''),
            color=0x5865F2
         )
         
         avatar_url = resposta.get('avatar_url')
         if avatar_url:
            embed.set_thumbnail(url=avatar_url)

         embed.add_field(name="Perfil", value=resposta.get('user_view_type', 'Não informado'), inline=True)
         embed.add_field(name="Seguidores", value=resposta.get('followers', 0), inline=True)
         embed.add_field(name="Repositórios Públicos", value=resposta.get('public_repos', 0), inline=True)
         works = api.consulta_projetos(pagina=1)
         last_works = '\n'.join(w.get('name', 'SEM NOME') for w in works)
         embed.add_field(
            name="Últimos projetos",
            value=last_works,
            inline=False
         )

         await interaction.followup.send(embed=embed, ephemeral=True)
        
      except requests.exceptions.RequestException as e:
         await interaction.followup.send(f'A API falhou: {e}', ephemeral=True)

async def setup(bot):
   await bot.add_cog(SlashComandos(bot))