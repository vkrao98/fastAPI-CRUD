from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
import uvicorn
from bson.objectid import ObjectId
import pprint
from pydantic import BaseModel
app = FastAPI()


conn = MongoClient("mongodb://localhost:27017")
db = conn["MongoDB"]
collection = db["menucards"]





def menucard_helper(menucard) -> dict:
    return {
        "id": str(menucard["_id"]),
        "gtb_rstrnt_name": menucard["gtb_rstrnt_name"],
        "gtb_item_name": menucard["gtb_item_name"],
        "primary_city": menucard["primary_city"],
        "state": menucard["state"],
        "cuisine": menucard["cuisine"],
    }

# Get all items names by text search in MongoDB

@app.get("/menu/{user_input}")
async def get_items(user_input: str) -> list:
    collection.create_index([('gtb_rstrnt_name', 'text')])
    my_query = {"$text": {"$search": user_input}}
    menucard = collection.find(my_query)
    my_list = []
    for x in menucard:
        my_list.append(menucard_helper(x))
    return my_list

# Get all cities and items of same location.my_list

# @app.get("/fooditems/{items}")
# async def get_items(primary_city: str, items: str) -> list:
#     # collection.create_index([('gtb_rstrnt_name', 'text')])
#     query2 = collection.find({"primary_city": primary_city})
#     my_query = {"$text": {"$search": items}}
#     menucard = collection.find(my_query)
#     my_list = []
#     for x in menucard:
#         my_list.append(menucard_helper(x))
#     for x in query2:
#         my_list.append(menucard_helper(x))
#     return my_list


# Get city names and food items based on User Input...

@app.get("/cityandfoodnames/{city}")
async def rtrv_items(primary_city: str, items: str) -> list:
    menucard = collection.find( {
        "$and": [ 
            {"primary_city": primary_city},
            {"$text": {"$search": items}} ] 
            })
    my_list = []
    for x in menucard:
        my_list.append(menucard_helper(x))
    return my_list



@app.get("/rstrnts/{primary_city}")
async def get_rstrnt_names(primary_city: str) -> list:
    my_query = {"primary_city": primary_city}
    menucard = collection.find(my_query)
    my_list = []
    for x in menucard:
        my_list.append(menucard_helper(x))
    return my_list

@app.get("/data/{id}")
async def retrieve_menucard(id: str) -> dict:
    menucard = collection.find_one({"_id": ObjectId(id)})
    if menucard:
        return menucard_helper(menucard)


# Get all the restaurant names based on primary_city:

@app.get("/names/{state}")
async def get_hotel_names(state: str) -> list:
    my_query = { "state": state}
    menucard = collection.find(my_query)
    my_list = []
    for x in menucard:
        my_list.append(menucard_helper(x))
    return my_list




# Welcome Message from the Root 

@app.get("/", tags=["/Root"])
async def call_root():
	return {"message":"Shri RAM "}


if __name__ == "__main__":
	uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
