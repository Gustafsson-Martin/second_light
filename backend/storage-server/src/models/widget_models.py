from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from .custom_types import PyObjectId, ObjectIdStr


class WidgetDatabaseModel(BaseModel):
    type: str
    left: float
    top: float
    width: float
    height: float
    settings: Dict
    contentid: PyObjectId


class WidgetContentDatabaseModel(BaseModel):
    content: Dict


class WidgetIdResponseModel(BaseModel):
    id: ObjectIdStr


class WidgetCreateModel(BaseModel):
    type: str
    left: float = 100.0
    top: float = 100.0
    width: float = 200.0
    height: float = 200.0
    settings: Dict = {}
    content: Dict = {}
    class Config:
        schema_extra = {
            "example": {
                "type": "ClockWidget",
                "left": 365.67,
                "top": 600.78,
                "width": 69.78,
                "height": 100.78,
                "content": {
                    "todolist": [{"content": "item", "checked": False}]
                }
            }
        }


class WidgetCreateSharedModel(BaseModel):
    widgetid: PyObjectId
    class Config:
        schema_extra = {
            "example": {
                "widgetid": "628616c94b57ad51aa3eafb8"
            }
        }


class WidgetUpdateModel(BaseModel):
    id: PyObjectId
    left: float
    top: float
    width: float
    height: float
    settings: Dict
    content: Dict = {}
    class Config:
        schema_extra = {
            "example": {
                "id": "62668fc990966b1b0bb9f27c",
                "left": 365.67,
                "top": 600.78,
                "width": 69.78,
                "height": 100.78,
                "content": {
                    "todolist": [{"content": "item", "checked": True}]
                }
            }
        }


class WidgetResponseModel(BaseModel):
    #id: ObjectIdStr = Field(..., alias="_id")
    type: str
    left: float
    top: float
    width: float
    height: float
    settings: Dict = {}
    content: Dict = {}
