
from bson import ObjectId
from fastapi import HTTPException
from pymongo import MongoClient
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from starlette.responses import JSONResponse


conn = MongoClient("mongodb://localhost:27017/")
db = conn["MongoDB"]
collection = db["menucards"]

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client["MongoDB"]

menucard_collection = database.get_collection("menucards")


# helpers
def menucard_helper(menucard) -> dict:
    return {
        "id": str(menucard["_id"]),
        "gtb_rstrnt_name": menucard["gtb_rstrnt_name"],
        "gtb_item_name": menucard["gtb_item_name"],
        "primary_city": menucard["primary_city"],
        "state": menucard["state"],
        "cuisine": menucard["cuisine"],
    }


# Retrieve all students present in the database
async def retrieve_menucards():
    menucards = []
    async for menucard in menucard_collection.find():
        menucards.append(menucard_helper(menucard))
    return menucards

async def rtrv_data(primary_city : str):

    menucards = []
    async for k , v in menucard_collection.find():
        if( k == "primary_city" & v == primary_city):
            menucards.append({"Restaurant Name":f"{v}"})
    return JSONResponse(status_code=200, content=jsonable_encoder(menucards))


# Add a new student into to the database
async def add_menucard(menucard_data: dict) -> dict:
    menucard = await menucard_collection.insert_one(menucard_data)
    new_menucard = await menucard_collection.find_one({"_id": menucard.inserted_id})
    return menucard_helper(new_menucard)


# Retrieve a student with a matching ID
async def retrieve_menucard(id: str) -> dict:
    menucard = await menucard_collection.find_one({"_id": ObjectId(id)})
    if menucard:
        return menucard_helper(menucard)

#Get the City Names
async def rtrv_cty_names(primary_city: str):
    menucard = await menucard_collection.find_one({"primary_city": primary_city}, {"primary_city": 1})
    if menucard:
        return menucard_helper(menucard)

# Update a student with a matching ID
async def update_menucard(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    menucard = await menucard_collection.find_one({"_id": ObjectId(id)})
    if menucard:
        updated_menucard = await menucard_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_menucard:
            return True
        return False

async def rtrv_rstrnts(primary_city : str) -> dict:

    try:
        menucard = menucard_collection.find_one({"primary_city": primary_city})
        for items in menucard:
            if items:
                return menucard_helper(items)
    except HTTPException as e:
        str(e)


# Delete a student from the database
async def delete_menucard(id: str):
    menucard = await menucard_collection.find_one({"_id": ObjectId(id)})
    if menucard:
        await collection.delete_one({"_id": ObjectId(id)})
        return True
