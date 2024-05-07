from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Any, Dict, TypedDict
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

discord_token = os.getenv("DISCORD_TOKEN", "")
mongodb_connection = os.getenv("MONGODB_CONNECTION", "")
if discord_token == "" and mongodb_connection == "":
    print("hello")
    with open(".env", "w") as f:
        f.write("DISCORD_TOKEN=\"\"\n")
        f.write("MONGODB_CONNECTION=\"\"\n")
    print("Please set the DISCORD_TOKEN and MONGODB_CONNECTION in the .env file")
    raise ValueError("DISCORD_TOKEN or MONGODB_CONNECTION not set")


Context = commands.Context[commands.Bot | commands.AutoShardedBot]


class Duration(TypedDict):
    hours: int
    days: int


class Event(TypedDict):
    title: str
    start: str
    finish: str
    duration: Duration
    url: str
    logo: str
    format: str
    onsite: bool


DEFAULT_PREFIX = "$"

client: MongoClient[Dict[str, Any]] = MongoClient(mongodb_connection)


ctfdb = client["ctftime"]  # Create ctftime database
ctfs: Collection[Event] = ctfdb["ctfs"]  # type:ignore | Create ctfs collection

teamdb = client["ctfteams"]  # Create ctf teams database

serverdb = client["serverinfo"]  # configuration db
