import disnake
from disnake.ext import commands
from random import choice, shuffle
from numpy import array
from asyncio import TimeoutError
from emojis import dance
from itertools import cycle
from buttons import TicTacToeGame, RPSGames


class Games(commands.Cog):
    """ Play games with your friends """

    def __init__(self, Intensity: commands.Bot):
        self.Intensity = Intensity

    @commands.command()
    @commands.guild_only()
    async def rps(self, ctx, *, player: disnake.Member):
        """Start a game of rock-paper-scissors with your friends"""
        view = RPSGames(ctx.author, player)
        await ctx.send(content="**Let the game Begin**", view=view)

    @rps.error
    async def rps_error(self, ctx, error):
        print(error)

    @commands.group(name="tictactoe", aliases=['ttt', 'tic'])
    @commands.guild_only()
    async def tictactoe(self, ctx, player: disnake.Member):
        """Play a game of ticactoe with your buddy"""
        emojis = ["<:ttt_x:902516406090878976>", "<:ttt_y:902515608640434198>"]
        players = [ctx.author, player]
        button_types = [disnake.ButtonStyle.green,
                        disnake.ButtonStyle.blurple]
        shuffle(emojis)
        shuffle(players)
        shuffle(button_types)
        game = cycle(zip(players, emojis, button_types))
        current_game = next(game)
        view = TicTacToeGame(game, current_game)
        await ctx.send(content=f"It's your turn {current_game[0].mention}", view=view)


def setup(Intensity):
    Intensity.add_cog(Games(Intensity))
