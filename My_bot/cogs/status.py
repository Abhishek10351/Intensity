import nextcord
from nextcord.ext import commands, tasks
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

    @tasks.loop(minutes=10)
    async def random_status(self):
        await self.Intensity.wait_until_ready()
        status = ['dnd', 'idle']
        while not self.Intensity.is_closed():
            activity = nextcord.Activity(
                type=nextcord.ActivityType.listening, name="Youtube Music")
            await self.Intensity.change_presence(activity=activity, status=choice(status))
            await asyncio.sleep(600)


def setup(Intensity):
    Intensity.add_cog(Status(Intensity))
