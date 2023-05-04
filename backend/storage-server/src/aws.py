from bson import ObjectId
import boto3
import os

ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
S3_BUCKET_NAME = "second-light-background-images"

s3_resource = boto3.resource(
    "s3",
    region_name = "eu-north-1",
    aws_access_key_id = ACCESS_KEY_ID,
    aws_secret_access_key = SECRET_ACCESS_KEY
)

s3_bucket = s3_resource.Bucket(S3_BUCKET_NAME)

s3_client = boto3.client(
    "s3",
    region_name = "eu-north-1",
    aws_access_key_id = ACCESS_KEY_ID,
    aws_secret_access_key = SECRET_ACCESS_KEY
)


def generate_filename():
    return str(ObjectId()) + ".jpg"


def generate_presigned_put_url(userid: str):
    return s3_client.generate_presigned_url(
        "put_object",
        Params = {
            "Bucket": S3_BUCKET_NAME,
            "Key": userid + "/" + generate_filename()
        },
        ExpiresIn = 100
    )


def generate_presigned_get_url(key: str):
    return s3_client.generate_presigned_url(
        "get_object",
        Params = {
            "Bucket": S3_BUCKET_NAME,
            "Key": key
        },
        ExpiresIn = 100
    )


def available_items(userid: str):
    items = []
    for item in s3_bucket.objects.filter(Prefix="default/"):
        print(item)
        if ".jpg" in item.key:
            items.append(item.key)
    for item in s3_bucket.objects.filter(Prefix=userid + "/"):
        print(item)
        if ".jpg" in item.key:
            items.append(item.key)
    return items
