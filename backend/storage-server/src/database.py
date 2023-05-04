import motor.motor_asyncio
import os

username = os.environ["STORAGE_DATABASE_ROOT_USERNAME"]
password = os.environ["STORAGE_DATABASE_ROOT_PASSWORD"]
uri = "second-light-storage-database:27017"
db_name = "second-light-storage"

db_uri = f"mongodb://{username}:{password}@{uri}/{db_name}?authSource=admin"

client = motor.motor_asyncio.AsyncIOMotorClient(db_uri)
db = client['second-light-storage']

widgets = db["widgets"]
widget_contents = db["widget_contents"]
users = db["users"]
