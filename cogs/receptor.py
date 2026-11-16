from aiohttp import web
from discord.ext import commands

class Receptor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.runner = None

    #roda automaticamente, quando se inicia o cog
    async def cog_load(self):
        app = web.Application()
        #quando chegar um POST ele chama o metodo receber
        app.router.add_post('/github', self.receber)

        #onde a porta do endereco é aberta
        self.runner = web.AppRunner(app)
        await self.runner.setup()
        #ele só aceita as requisições da maquina pessoal (temporariamente pae)
        site = web.TCPSite(self.runner, '127.0.0.1', 8080)
        await site.start()
        print('Receptor ouvindo!')

    #desliga o servidor, quando n ta usando mais o cog
    async def cog_unload(self):
        if self.runner:
            await self.runner.cleanup()
    #meio obvio
    async def receber(self, request):
        evento = request.headers.get('X-Gitub-Event')
        dados = await request.json()

        print(f'Webhook evento: {evento}')
        print(f'Webhook repositório: {dados.get("Repository", {}).get("full_name")}')

        return web.Response(text = 'ok')

async def setup(bot):
   await bot.add_cog(Receptor(bot))