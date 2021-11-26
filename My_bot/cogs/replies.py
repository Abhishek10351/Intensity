import nextcord
from nextcord.ext import commands
from random import choice
from emojis import dance, phil, no
from nextcord.utils import get
from numpy import array


class Reply(commands.Cog):
    def __init__(self, Intensity: commands.Bot):
        self.Intensity = Intensity

    @commands.Cog.listener("on_command_error")
    async def errors(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(embed=nextcord.Embed(description=f"**{error}**", colour=nextcord.Colour.red()))
        elif isinstance(error, commands.errors.RoleNotFound):
            await ctx.message.add_reaction('😬')
            await ctx.send(embed=nextcord.Embed(description=f"**{error.argument} is not a valid role**", colour=nextcord.Colour.red()))
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'**You\'re on cooldown try again in {round(error.retry_after)} seconds**')
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send('**This command works only on servers**')
        elif isinstance(error, commands.MissingPermissions):
            perms = error.missing_perms
            await ctx.send(f'**You don\'t have the {", ".join(perms)} permissions for this command**')
        elif isinstance(error, commands.BotMissingPermissions):
            bot_perms = error.missing_perms
            await ctx.send(f"**I don't have {', '.join(bot_perms)} permissions**")
        else:
            await ctx.send(error)


def setup(Intensity):
    Intensity.add_cog(Reply(Intensity))
