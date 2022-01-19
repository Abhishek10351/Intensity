import disnake
from disnake.ext import commands
import time
from sql import fetch
from timeit import timeit
from mongo import prefixes
from buttons import Paginator

class Misc(commands.Cog):

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
            fetch(f'select * from muted_roles where guild_ID = {ctx.author.id}')

        @timer
        def mongodb():
            prefixes.find_one({"_id": ctx.author.id})

        embed = disnake.Embed(description='**Ping**',
                              colour=disnake.Colour.random())
        embed.add_field(name='Discord Websocket <:discord:915501670979477524>',
                        value=f'`{round((self.Intensity.latency) * 1000)} ms`', inline=False)
        embed.add_field(
            name='Typing <a:typing:883235601187487824>', value=f'`{round(k*1000)} ms`', inline=False)
        embed.add_field(name='Sqlite3 Latency <:sqlite3:879576089238831145>',
                        value=f'`{round(sqldb()*1000)+1} ms`', inline=False)
        embed.add_field(name="MongoDB <:mongo_db:915501188978454568>",
                        value=f"`{round(mongodb()*1000)} ms`", inline=False)
        await a.edit(content='', embed=embed)
    
    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.channel)
    async def info(self, ctx):
        class Invite(disnake.ui.View):
            def __init__(self):
                super().__init__()
                self.add_item(disnake.ui.Button(label="Invite me",  url="https://discord.com/api/oauth2/authorize?client_id=852203850214801428&permissions=1394723912950&scope=bot"))
        embed = disnake.Embed(description="**Hey, I am Intensity a multi-purpose discord bot with many features**", colour=disnake.Colour.random())
        embed.add_field("Creator", "Peter parker#1716")
        embed.add_field("Library", "Disnake")
        embed.add_field("Server count", str(len(self.Intensity.guilds)))
        embed.add_field("User Count", str(len(self.Intensity.users)))
        await ctx.send(embed=embed, view=Invite())
    
    @commands.command(name="test", is_hidden=True)
    async def test(self, ctx):
        view = Paginator()
        await ctx.send(content=0, view=view)
    
    


def setup(Intensity):
    Intensity.add_cog(Misc(Intensity))
