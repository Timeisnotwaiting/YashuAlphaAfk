from os import getenv

from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

BOT_TOKEN = getenv("BOT_TOKEN")

MONGO_DB_URI = getenv("MONGO_DB_URI", None)

SUDO_USER = list(
    map(int, getenv("SUDO_USER", "").split())
) 

OWNER_USERNAME = getenv("OWNER_USERNAME", "@Timeisnotwaiting")

if OWNER_USERNAME[0] == "@":
    OWNER = OWNER_USERNAME[1:]
else:
    OWNER = OWNER_USERNAME
