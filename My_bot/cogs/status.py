import disnake
from disnake.ext import commands, tasks
import asyncio
from random import choice


class Status(commands.Cog):
    def __init__(self, Intensity):
        self.Intensity = Intensity
        self.ping_message.start()
        self.random_status.start()

    @tasks.loop(minutes=30)
    async def ping_message(self):
        await self.Intensity.wait_until_ready()
        while not self.Intensity.is_closed():
            await asyncio.sleep(1800)
            channel = self.Intensity.get_channel(870959477577359390)
            await channel.send(f'`{round(self.Intensity.latency * 1000)} s`')

    @tasks.loop(hours=1)
    async def random_status(self):
        await self.Intensity.wait_until_ready()
        while not self.Intensity.is_closed():
            game = disnake.Game(
            choice(['tic-tac-toe', 'with disnake bots', 'on 9 guilds', 'with Phil Swift', "football with your head"]))
            stream = disnake.Streaming(name=" Youtube", url=f"https://www.youtube.com/watch?v=raTkZqz680Y", platform='YouTube')
            await self.Intensity.change_presence(activity=choice([stream, game]))
            await asyncio.sleep(3600)


def setup(Intensity):
    Intensity.add_cog(Status(Intensity))
