from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from models.user_models import *
from database import users
from aws import generate_presigned_put_url, generate_presigned_get_url, available_items
from fastapi import Depends
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session


router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/",
        status_code = status.HTTP_200_OK,
        response_model = UserResponseModel)
async def user_get(session: SessionContainer = Depends(verify_session())):
    userid = session.get_user_id()
    return await users.find_one({"userid": userid})


@router.post("/create",
        status_code = status.HTTP_201_CREATED,
        response_model = UserResponseModel)
async def user_create(model: UserCreateModel, session: SessionContainer = Depends(verify_session())):
    userid = session.get_user_id()
    database_model = UserDatabaseModel(**model.dict(), userid=userid)
    user = await users.insert_one(database_model.dict())
    return await users.find_one({"_id": user.inserted_id})


@router.post("/username/set",
        status_code=status.HTTP_200_OK)
async def user_username_set(model: UserChangeUsernameModel, session: SessionContainer = Depends(verify_session())):
    userid = session.get_user_id()
    await users.update_one({"userid": userid}, {"$set": {"username": model.username}})
    return {"message": "success"}


@router.get("/background_image_upload_url",
        status_code=status.HTTP_200_OK)
async def background_image_upload_url(session: SessionContainer = Depends(verify_session())):
    userid = session.get_user_id()
    return {"url": generate_presigned_put_url(userid)}


@router.get("/background_image",
        status_code=status.HTTP_200_OK)
async def background_image(key: str, session: SessionContainer = Depends(verify_session())):
    return {"url": generate_presigned_get_url(key)}


@router.get("/available_background_images",
        status_code=status.HTTP_200_OK)
async def available_background_images(session: SessionContainer = Depends(verify_session())):
    userid = session.get_user_id()
    return {"items": available_items(userid)}


@router.post("/selected_backgrounds",
        status_code=status.HTTP_200_OK)
async def selected_backgrounds(model: UserSelectedBackgroundsModel, session: SessionContainer = Depends(verify_session())):
    userid = session.get_user_id()
    await users.update_one({"userid": userid}, {"$set": {"background_images": model.backgrounds}})
    return {"message": "success"}
