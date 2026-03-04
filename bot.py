from dotenv import load_dotenv
import os
load_dotenv()

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

temp_channels = {}

@bot.event
async def on_ready():
    print(f'TomyumBot is online!')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.name}! 👋')

@bot.command()
async def createroom(ctx, *, name="Temp Room"):
    if ctx.author.id in temp_channels:
        await ctx.send("You already have a room! Use !deleteroom first.")
        return
    channel = await ctx.guild.create_voice_channel(name=name)
    temp_channels[ctx.author.id] = channel.id
    await ctx.send(f'✅ Room **{name}** created!')

@bot.command()
async def deleteroom(ctx):
    if ctx.author.id not in temp_channels:
        await ctx.send("You don't have a room.")
        return
    channel = ctx.guild.get_channel(temp_channels[ctx.author.id])
    if channel:
        await channel.delete()
    del temp_channels[ctx.author.id]
    await ctx.send("🗑️ Room deleted.")

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel and before.channel.id in temp_channels.values():
        if len(before.channel.members) == 0:
            owner = [uid for uid, cid in temp_channels.items() if cid == before.channel.id]
            if owner:
                del temp_channels[owner[0]]
            await before.channel.delete()

bot.run(os.getenv('TOKEN'))