from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder


from db import (
    add_menucard,
    delete_menucard,
    retrieve_menucard,
    retrieve_cityNames,
    rtrv_rstrnts,
    rtrv_data,
    retrieve_menucards,
    update_menucard
)

from menucard import (
    ErrorResponseModel,
    ResponseModel,
    MenucardSchema,
    UpdateMenucardModel,
)

router = APIRouter()