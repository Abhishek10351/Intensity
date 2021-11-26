import nextcord
from nextcord.ext import commands
import time
from sql import fetch
from timeit import timeit


class misc(commands.Cog):

    def __init__(self, Intensity):
        self.Intensity = Intensity

    @commands.command(name='ping')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ping(self, ctx):
        """Ping"""
        def timer(f):
            def inner(*args):
                start = time.time()
                result = f(*args)
                return time.time() - start
            return inner
        k = time.time()
        a = await ctx.send('**Testing Ping**')
        k = time.time() - k

        @timer
        def database():
            fetch(f'select * from mute_roles where guild_id = {ctx.guild.id}')[
                0]

        embed = nextcord.Embed(description='**Ping**',
                               colour=nextcord.Colour.red())
        embed.add_field(name='Bot Latency',
                        value=f'`{round((self.Intensity.latency) * 1000)} ms`')
        embed.add_field(
            name='Typing Latency <a:typing:883235601187487824>', value=f'`{round(k*1000)} ms`')
        embed.add_field(name='Database Latency',
                        value=f'`{round(database()*1000)} ms`')
        await a.edit(content='', embed=embed)


def setup(Intensity):
    Intensity.add_cog(misc(Intensity))
