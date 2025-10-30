import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).parent.parent.parent  
ENV_PATH = ROOT_DIR / ".env"
if not ENV_PATH.exists():
    raise FileNotFoundError(f".env fajl nije pronađen na: {ENV_PATH}")

load_dotenv(dotenv_path=ENV_PATH)


MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

if not MONGO_URI or not DB_NAME:
    raise ValueError("MONGO_URI ili DB_NAME nisu definisani u .env fajlu!")


client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]


tasks_collection = db["tasks"]