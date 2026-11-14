import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER_ID = discord.Object(id=os.getenv('ID_SERVER'))

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)

@bot.event
async def on_ready():
    bot.tree.copy_global_to(guild=SERVER_ID)
    synced = await bot.tree.sync(guild=SERVER_ID)
    print(f"Comandos sincronizados instantaneamente no servidor: {len(synced)}")

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            cog_name = filename[:-3]
            await bot.load_extension(f'cogs.{cog_name}')
            print(f'[Módulo Carregado] cogs/{filename}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
