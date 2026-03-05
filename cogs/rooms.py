from discord.ext import commands


class Rooms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_channels = {}

    @commands.command()
    async def createroom(self, ctx, *, name="Temp Room"):
        if ctx.author.id in self.temp_channels:
            await ctx.send("You already have a room! Use !deleteroom first.")
            return
        channel = await ctx.guild.create_voice_channel(name=name)
        self.temp_channels[ctx.author.id] = channel.id
        await ctx.send(f'✅ Room **{name}** created!')

    @commands.command()
    async def deleteroom(self, ctx):
        if ctx.author.id not in self.temp_channels:
            await ctx.send("You don't have a room.")
            return
        channel = ctx.guild.get_channel(self.temp_channels[ctx.author.id])
        if channel:
            await channel.delete()
        del self.temp_channels[ctx.author.id]
        await ctx.send("🗑️ Room deleted.")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel and before.channel.id in self.temp_channels.values():
            if len(before.channel.members) == 0:
                owner = [uid for uid, cid in self.temp_channels.items() if cid == before.channel.id]
                if owner:
                    del self.temp_channels[owner[0]]
                await before.channel.delete()


async def setup(bot):
    await bot.add_cog(Rooms(bot))
