import disnake
from disnake.ext import commands
from random import choice
from emojis import dance, phil, no
from disnake.utils import get
from numpy import array


class Reply(commands.Cog):
    def __init__(self, Intensity: commands.Bot):
        self.Intensity = Intensity

    @commands.Cog.listener("on_command_error")
    async def errors(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, (commands.MemberNotFound, commands.errors.RoleNotFound)):
            await ctx.send(embed=disnake.Embed(description=f"**{error}**", colour=disnake.Colour.red()))
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=disnake.Embed(description=f'**You\'re on cooldown try again in {round(error.retry_after)} seconds**'))
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(embed=disnake.Embed(description='**This command works only on servers**'))
        elif isinstance(error, commands.MissingPermissions):
            pass
        elif isinstance(error, commands.BotMissingPermissions):
            bot_perms = error.missing_permissions
            await ctx.send(embed=disnake.Embed(description=f"**I don't have {', '.join(bot_perms)} permissions**"))
        else:
            await ctx.send(f"**{error}**")


def setup(Intensity):
    Intensity.add_cog(Reply(Intensity))
