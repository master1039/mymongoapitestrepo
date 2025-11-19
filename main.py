from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client["mydb"]
collection = db["mydb_collection"]

app = FastAPI()

class my_collection(BaseModel):
    name: str
    phone:int
    city: str
    course: str

@app.post("/euron/insert")
async def mydb_data_insert(data:my_collection):
    result = await collection.insert_one(data.dict())
    return {"inserted_id": str(result.inserted_id)}

# MongoDB connection string
@app.get("/euron/getdata")
async def get_euron_data():
    items = []
    cursor = collection.find({})
    async for document in cursor:
        document["_id"] = str(document["_id"])
        items.append(document)
    return items
        