import os
from typing import Any, Dict

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection

from common import EventT

load_dotenv()

SRC_URL = "https://github.com/FieryRMS/TuningBot"

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
MONGODB_CONNECTION = os.getenv("MONGODB_CONNECTION", "")
if DISCORD_TOKEN == "" and MONGODB_CONNECTION == "":
    with open(".env", "w") as f:
        f.write('DISCORD_TOKEN=""\n')
        f.write('MONGODB_CONNECTION=""\n')
    print("Please set the DISCORD_TOKEN and MONGODB_CONNECTION in the .env file")
    raise ValueError("DISCORD_TOKEN or MONGODB_CONNECTION not set")


DEFAULT_PREFIX = "$"


client: MongoClient[Dict[str, Any]] = MongoClient(MONGODB_CONNECTION)

ctfdb = client["ctftime"]  # Create ctftime database
ctfs: Collection[EventT] = ctfdb[
    "ctfs"
]  # pyright: ignore[reportAssignmentType] | Create ctfs collection

teamdb = client["ctfteams"]  # Create ctf teams database

serverdb = client["serverinfo"]  # configuration db
