"""Main file for the API"""

import uuid
import json
import boto3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_secrets():
    """ Get value of secret from AWS Secrets Manager """

    secret = boto3.client('secretsmanager')
    response = secret.get_secret_value(
        SecretId='personal-website-secret'
    )
    return json.loads(response['SecretString'])

secrets = get_secrets()
table_name = secrets['table_name']

@app.get("/")
async def root():
    """Root healthcheck endpoint"""

    return {"message": "Hello World"}


@app.post("/create_cafe")
async def create_new_cafe(cafe: dict):
    """Endpoint for POST request to add to database"""

    dynamodb = boto3.client('dynamodb')
    response = dynamodb.put_item(
        TableName=table_name,
        Item={
            "id": {"S": str(uuid.uuid4())},
            "shop_name": {"S": cafe['shop_name']},
            "latitude": {"N": cafe['latitude']},
            "longitude": {"N": cafe['longitude']},
        },
    )

    if response['HTTPStatusCode'] == 200:
        return {"message": "New cafe created"}

    return {"message": "Error creating new cafe"}


@app.put("/update_cafe")
async def update_cafe():
    """Endpoint for PUT request to update database"""

    return {"message": "Cafe has been updated"}
