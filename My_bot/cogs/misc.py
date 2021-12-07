import nextcord
from nextcord.ext import commands
import time
from sql import fetch
from timeit import timeit
from mongo import prefixes


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
        def sqldb():
            fetch(f'select * from muted_roles where guild_id = {ctx.guild.id}')

        @timer
        def mongodb():
            prefixes.find_one({"_id": ctx.guild.id})

        embed = nextcord.Embed(description='**Ping**',
                               colour=nextcord.Colour.red())
        embed.add_field(name='Discord Websocket Latency <:discord:915501670979477524>',
                        value=f'`{round((self.Intensity.latency) * 1000)} ms`')
        embed.add_field(
            name='Typing Latency <a:typing:883235601187487824>', value=f'`{round(k*1000)} ms`')
        embed.add_field(name='Sqlite3 Latency <:sqlite3:879576089238831145>',
                        value=f'`{round(sqldb()*1000)} ms`')
        embed.add_field(name="MongoDB Latency <:mongo_db:915501188978454568>",
                        value=f"`{round(mongodb()*1000)} ms`", inline=True)
        await a.edit(content='', embed=embed)


def setup(Intensity):
    Intensity.add_cog(misc(Intensity))
