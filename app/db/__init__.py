import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load .env from root
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

if not MONGO_URI or not DB_NAME:
    raise ValueError("MONGO_URI or DB_NAME not defined in .env")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

tasks_collection = db["tasks"]
