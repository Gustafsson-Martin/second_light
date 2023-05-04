from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from .custom_types import PyObjectId, ObjectIdStr


class UserDatabaseModel(BaseModel):
    userid: str
    username: str
    widgets: List[PyObjectId]
    background_images: List[str]


class UserCreateModel(BaseModel):
    username: str = ""
    widgets: List[PyObjectId] = []
    background_images: List[str] = []
    class Config:
        schema_extra = {
            "example": {
                "username": "MyGreatUsername"
            }
        }


class UserResponseModel(BaseModel):
    id: ObjectIdStr = Field(..., alias="_id")
    userid: str
    username: str
    widgets: List[ObjectIdStr]
    background_images: List[str]


class UserChangeUsernameModel(BaseModel):
    username: str
    class Config:
        schema_extra = {
            "example": {
                "username": "MyGreatUsername"
            }
        }


class UserSelectedBackgroundsModel(BaseModel):
    backgrounds: List[str]
