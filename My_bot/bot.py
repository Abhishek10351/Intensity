import logging
import datetime
import time
from disnake.ext import commands
import disnake
from pathlib import Path
from random import choice
from sql import execute, fetch
from disnake import utils
from dotenv import load_dotenv
from os import getenv
from HelpCommand import CustomHelpCommand
from mongo import prefixes
from webserver import keep_alive

intents = disnake.Intents.all()

logging.basicConfig(level=logging.INFO)
load_dotenv()


class Intensity(commands.Bot):
    """Main Bot class to control the bot"""

    def __init__(self):
        super().__init__(command_prefix=',', case_insensitive=True, intents=intents,
                         owner_ids = getenv("owner_ids"), help_command=CustomHelpCommand())

    def run(self):
        """ Bring the bot online """
        print("Running..", end='\r')
        super().run(getenv("bot_token"))

    async def get_prefix(bot, message):
        """ Returns a prefix for the bot """
        if message.guild is not None:
            try:
                prefix = prefixes.find_one({"_id": message.guild.id})["prefix"]
            except Exception as e:
                prefixes.insert_one({"_id": message.guild.id, "prefix": ","})
                prefix = (',')
        else:
            prefix = (',')
        return commands.when_mentioned_or(prefix)(bot, message)

    async def on_ready(self):
        print('Logged in ', end='\r')
        
        print('I am ready')

#keep_alive()
bot = Intensity()
all_cogs = [p.stem for p in Path("cogs").glob("*.py")]
for cog in all_cogs:
    bot.load_extension(f"cogs.{cog}")
bot.starttime = time.time()
bot.run()
