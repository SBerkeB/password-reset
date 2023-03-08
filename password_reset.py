from fastapi import APIRouter, Form, Request
from starlette.responses import FileResponse
from bson.objectid import ObjectId

import jwt
import time

jwtSecret = "berke"
router = APIRouter(prefix="/password-change")


def jwtDecoder(encoded):
    decoded = jwt.decode(encoded, jwtSecret, algorithms=["HS256"])
    return decoded


@router.post("/{jwt_code}")
async def passwordReset(jwt_code: str,request: Request, newPassword: str = Form(), newPasswordCheck: str = Form()):
    decoded = jwtDecoder(jwt_code)
    if newPassword == newPasswordCheck:
        new_password = { "$set": { 'password': newPassword } }
        request.app.database["users"].update_one({"_id": ObjectId(decoded["_id"])}, new_password)
        return FileResponse("success.html")
    else:
        return {"message": "Your password does not match!"}
    
@router.get("/{jwt_code}")
async def resetPage(jwt_code: str):
    if time.time() - jwtDecoder(jwt_code)["timestamp"] < 300:
        return FileResponse("change.html")
    else:
        return {"message": "Your code has expired"}