import discord
from discord.ext import commands

class Geral(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Exemplo de um evento específico deste módulo (opcional)
    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Mínimo esqueleto: personalize aqui o que acontece quando alguém entra
        pass

    # Exemplo de um comando base com prefixo (ex: !ping)
    @commands.command(name='ping', help='Responde com Pong e a latência.')
    async def ping(self, ctx):
        latencia = round(self.bot.latency * 1000)
        await ctx.send(f'Pong! 🏓 ({latencia}ms)')

# Função obrigatória do discord.py para registrar a Cog no bot principal
async def setup(bot):
    await bot.add_cog(Geral(bot))