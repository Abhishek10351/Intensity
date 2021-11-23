from pymongo import MongoClient
from os import getenv
from dotenv import load_dotenv
load_dotenv()
cluster = MongoClient(getenv("mongo_token"))
commands = cluster.discord.commands
prefixes = cluster.discord.prefix