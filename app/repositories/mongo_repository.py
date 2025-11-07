from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

class MongoRepository:
    def __init__(self, db_client: AsyncIOMotorClient, collection_name: str):
        """
        db_client: instance AsyncIOMotorClient
        collection_name: ime kolekcije u bazi
        """
        self.collection = db_client[collection_name]  

    async def insert_one(self, data: dict) -> str:
        result = await self.collection.insert_one(data)
        return str(result.inserted_id)

    async def find_one(self, query: dict) -> dict | None:
        doc = await self.collection.find_one(query)
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def find_by_id(self, id: str) -> dict | None:
        doc = await self.collection.find_one({"_id": ObjectId(id)})
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def delete_by_id(self, id: str) -> int:
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count

    async def find_all(self) -> list[dict]:
        docs = []
        cursor = self.collection.find()
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            docs.append(doc)
        return docs
