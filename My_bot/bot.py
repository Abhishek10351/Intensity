import logging
import datetime
import time
from nextcord.ext import commands
import nextcord
from pathlib import Path
from random import choice
from sql import execute, fetch
from nextcord import utils
from dotenv import load_dotenv
from os import getenv
from HelpCommand import CustomHelpCommand
from mongo import prefixes
intents = nextcord.Intents.all()

logging.basicConfig(level=logging.INFO)



class Intensity(commands.Bot):
    """Main Bot class to control the main bot"""

    def __init__(self):
        super().__init__(command_prefix=',', case_insensitive=True, intents=intents,
                         owner_ids=[707107037070360596], help_command=CustomHelpCommand())

    def run(self):
        """ Bring the bot online """
        load_dotenv()
        print("Running..", end='\r')
        super().run(getenv("bot_token"))

    async def get_prefix(bot, message):
        """ Returns a prefix for the bot """
        if message.guild is not None:
            try:
                prefix = prefixes.find_one({"_id":message.guild.id})["prefix"]
            except Exception as e:
                prefixes.insert_one({"_id": message.guild.id, "prefix": ","})
                prefix = (',')
        else:
            prefix = (',')
        return commands.when_mentioned_or(prefix)(bot, message)

    async def on_ready(self):
        print('Logged in ', end='\r')
        all_cogs = [p.stem for p in Path("cogs").glob("*.py")]
        for cog in all_cogs:
            self.load_extension(f"cogs.{cog}")
        print("Cogs loaded successfully!")
        game = nextcord.Game(
            choice(['tic-tac-toe', 'with nextcord bots', 'on 9 guilds', 'with Phil Swift']))
        # await self.change_presence(activity=nextcord.Streaming(name=" youtube", url=f"https://www.youtube.com/watch?v=raTkZqz680Y", platform='YouTube'))
        print('I am ready')


bot = Intensity()
bot.starttime = time.time()
bot.run()

# github.com/pokeapi
