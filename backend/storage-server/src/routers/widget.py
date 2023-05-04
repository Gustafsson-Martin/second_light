from fastapi import APIRouter, status, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from models.widget_models import *
from database import users, widgets, widget_contents
from collections import ChainMap
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/widget",
    tags=["widget"]
)

#TODO: Do some error handling in this file

#TODO: Understand why I can't return "_id" with model
@router.get("/",
        status_code = status.HTTP_200_OK,
        response_model = WidgetResponseModel)
async def widget_get(id: PyObjectId, session: SessionContainer = Depends(verify_session())):
    widget = await widgets.find_one({"_id": id})
    if not widget:
        return JSONResponse(status_code=400, content={"message": "Widget does not exist"})
    content = await widget_contents.find_one({"_id": widget["contentid"]})
    return WidgetResponseModel(**ChainMap(widget, content))


@router.post("/create",
        status_code = status.HTTP_201_CREATED,
        response_model = WidgetIdResponseModel)
async def widget_create(model: WidgetCreateModel, session: SessionContainer = Depends(verify_session())):
    userid = session.get_user_id()
    content = await widget_contents.insert_one(WidgetContentDatabaseModel(**model.dict()).dict())
    widget = await widgets.insert_one(WidgetDatabaseModel(**model.dict(), contentid=content.inserted_id).dict())
    await users.update_one({"userid": userid}, {"$push": {"widgets": widget.inserted_id}})
    return {"id": widget.inserted_id}


@router.post("/create/shared",
        status_code = status.HTTP_201_CREATED,
        response_model = WidgetIdResponseModel)
async def widget_create_shared(model: WidgetCreateSharedModel, session: SessionContainer = Depends(verify_session())):
    userid = session.get_user_id()
    widget = await widgets.find_one({"_id": model.widgetid})
    if not widget:
        return JSONResponse(status_code=400, content={"message": "Widget does not exist"})
    widget = await widgets.insert_one(WidgetDatabaseModel(**widget).dict())
    await users.update_one({"userid": userid}, {"$push": {"widgets": widget.inserted_id}})
    return {"id": widget.inserted_id}


@router.post("/update",
        status_code = status.HTTP_200_OK)
async def widget_update(model: WidgetUpdateModel, session: SessionContainer = Depends(verify_session())):
    widget = await widgets.find_one({"_id": model.id})
    if not widget:
        return JSONResponse(status_code=400, content={"message": "Widget does not exist"})
    await widget_contents.update_one({"_id": widget["contentid"]}, {"$set": {"content": model.content}})
    await widgets.update_one({"_id": model.id}, {"$set": model.dict(exclude={'id','content'})})
    return {"message": "success"}
