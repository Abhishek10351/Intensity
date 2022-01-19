import disnake
from disnake.ext import commands
from pandas import DataFrame, read_csv
from random import randint, choice
from numpy import int64
from emojis import no
import asyncio
from typing import Union, Optional
from randfacts import get_fact


class Fun(commands.Cog):
    def __init__(self, Intensity: commands.Bot):
        self.Intensity = Intensity

    

    @commands.command(name='tts', aliases=['say'])
    @commands.guild_only()
    @commands.has_permissions(send_tts_messages=True)
    @commands.bot_has_permissions(send_tts_messages=True)
    async def tts(self, ctx: commands.Context, *, message=None):
        """Converts your text message to `text to speech` message """
        if message is not None:
            await ctx.send(message, tts=True)
        else:
            await ctx.send('**Idiot enter something to covert to tts**')

    @commands.command(aliases=['fact', 'facts'])
    @commands.guild_only()
    async def randfact(self, ctx, type: Optional[str] = None):
        """Get a random fact"""
        fact = get_fact()
        embed = disnake.Embed(title="That's a fact",
                              description=f'**{fact}**', colour=disnake.Color.random())
        await ctx.send(embed=embed)


def setup(Intensity):
    Intensity.add_cog(Fun(Intensity))
