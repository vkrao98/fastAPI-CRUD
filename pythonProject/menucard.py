from typing import Optional

from pydantic import BaseModel,Field


class MenucardSchema(BaseModel):
    gtb_rstrnt_name: str = Field(...)
    primary_city: str = Field(...)
    state: str = Field(...)
    gtb_item_name: str = Field(...)
    cuisine: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "gtb_rstrnt_name": "Diamond Bawarchi",
                "primary_city": "Dallas",
                "state": "TX",
                "gtb_item_name": "Chicken Biryani",
                "cuisine": "Indian",
            }
        }


class UpdateMenucardModel(BaseModel):
    gtb_rstrnt_name: Optional[str]
    primary_city: Optional[str]
    state: Optional[str]
    gtb_item_name: Optional[str]
    cuisine: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "gtb_rstrnt_name": "Diamond Bawarchi",
                "primary_city": "Dallas",
                "state": "TX",
                "gtb_item_name": "Chicken Biryani",
                "cuisine": "Indian",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def responseModel(data, message):
    return {
        "data": {data},
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}