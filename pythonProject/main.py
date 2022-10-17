from fastapi import FastAPI, Body, HTTPException
import uvicorn
from fastapi.encoders import jsonable_encoder
from mongoengine import connect
from starlette.responses import JSONResponse

from db import retrieve_menucards, retrieve_menucard, rtrv_data, retrieve_cityNames, update_menucard, delete_menucard, add_menucard
# from fastapi.responses import JSONResponse

from menucard import ResponseModel, MenucardSchema, ErrorResponseModel, UpdateMenucardModel, responseModel
from menucardRoutes import router as MenucardRouter, router

connect(host="mongodb://127.0.0.1:27017/MongoDB")

app = FastAPI()
app.include_router(MenucardRouter, tags=["Menucard"], prefix="/menucard")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}



@router.post("/", response_description="Menucard data added into the database")
async def add_menucard_data(menucard: MenucardSchema = Body(...)):
    menucard = jsonable_encoder(menucard)
    new_menucard = await add_menucard(menucard)
    return ResponseModel(new_menucard, "Menucard added successfully.")


@router.get("/", response_description="Menucards retrieved")
async def get_menucards():
    menucards = await retrieve_menucards()
    if menucards:
        return ResponseModel(menucards, "Menucards data retrieved successfully")
    return ResponseModel(menucards, "Empty list returned")


@router.get("/{id}", response_description="Menucards data retrieved")
async def get_menucard_data(id):
    menucard = await retrieve_menucard(id)
    if menucard:
        return ResponseModel(menucard, "Menucard data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")

@router.get("/{NewApproachforFind}")
async def get_rstrnt_names(primary_city : str):
    menucard =  rtrv_data(primary_city)
    if menucard:
        return ResponseModel(menucard,"City Names got")
    return ErrorResponseModel("Error ", 404, "Not VAles")


@router.get("/{primary_city}", response_description="Restaurant Names data retrieved successfully")
async def get_cityName_data():
    # print(primary_city)
    try:
        menucard = await retrieve_cityNames()
        if menucard:
            return JSONResponse(content=jsonable_encoder(menucard))
    except HTTPException as e:
        return str(e)

# @app.get("/cities/")
# async def cities(primary_city):
#     menucards = json.loads(Menucards.objects.filter(primary_city__icontains = primary_city).to_json())
#    async for key , val in menucards[0].items():
#         if (key == "gtb_rstrnt_name"):
#             return JSONResponse(status_code = 200, content={"Restaurant Name":f"{val}","Menus": menucards})
#
#         else:
#             return JSONResponse(status_code=200, content="ERROR NOT FOUND!!!")




@router.put("/{id}")
async def update_menucard_data(id: str, req: UpdateMenucardModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_menucard = await update_menucard(id, req)

    if updated_menucard:
        return ResponseModel(
            "Menucard with ID: {} name update is successful".format(id),
            "Menucard name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the menucard data.",
    )


@router.delete("/{id}", response_description="Menucard data deleted from the database")
async def delete_menucard_data(id: str):
    deleted_menucard = await delete_menucard(id)
    if deleted_menucard:
        return ResponseModel(
            "Menucard with ID: {} removed".format(id), "Menucard deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Menucard with id {0} doesn't exist".format(id)
    )





if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
