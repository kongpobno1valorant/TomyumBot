import discord
from discord.ext import commands


class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title=guild.name, color=discord.Color.blue())
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name='Owner', value=guild.owner.mention)
        embed.add_field(name='Members', value=guild.member_count)
        embed.add_field(name='Channels', value=len(guild.channels))
        embed.add_field(name='Roles', value=len(guild.roles))
        embed.add_field(name='Created', value=guild.created_at.strftime('%d %b %Y'))
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ServerInfo(bot))
