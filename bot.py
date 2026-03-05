import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

COGS = [
    'cogs.general',
    'cogs.rooms',
    'cogs.serverinfo',
]


@bot.event
async def on_ready():
    print(f'TomyumBot is online!')


async def main():
    async with bot:
        for cog in COGS:
            await bot.load_extension(cog)
        await bot.start(os.getenv('TOKEN'))


asyncio.run(main())
