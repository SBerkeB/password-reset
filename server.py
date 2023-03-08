from fastapi import FastAPI, Form, Request
from starlette.responses import FileResponse
from dotenv import dotenv_values
from pymongo import MongoClient

import user_check 
import password_reset
import uuid

import certifi

config = dotenv_values(".env")

app = FastAPI()

app.include_router(user_check.router)
app.include_router(password_reset.router)

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"], tlsCAFile=certifi.where())
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    

@app.post("/")
async def getUserInfo(request: Request, username: str = Form(), password: str = Form()):
    obj = {"username": username, "password": password}
    print("hi")
    request.app.database["users"].insert_one(obj)
    
    return {"message": "Successfully signed up!"}

@app.get("/")
async def pageLoader():
    return FileResponse("form.html")
    