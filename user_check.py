from fastapi import APIRouter, Form, Request
from starlette.responses import FileResponse
from botocore.exceptions import ClientError

import jwt
import boto3
import time



SENDER = "samiberke2003@gmail.com"
RECIPIENT = "samiberke2003@gmail.com"
AWS_REGION = "us-east-1"
SUBJECT = "Amazon SES Test (SDK for Python)"
CHARSET = "UTF-8"


jwtSecret = "berke"
router = APIRouter(prefix="/user-info")



def jwtEncoder(obj):
    encoded = jwt.encode(obj, jwtSecret, algorithm="HS256")
    return encoded

def mailSender(jwt):
    BODY_HTML = """
    <!DOCTYPE html>
    <html>
    <head></head>
    <body>
    <h1>Amazon SES Test (SDK for Python)</h1>
        <a href='http://127.0.0.1:8000/password-change/{encoded}'>Click Here<a>
    </body>
    </html>
                """.format(encoded=jwt)
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                )
    client = boto3.client('ses',region_name=AWS_REGION)

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
    return



@router.post("/")
async def getUserInfo(request: Request, username: str = Form()):
    if (user := request.app.database["users"].find_one({"username": username})) is not None:
        obj = {"username": username, "timestamp": int(time.time()), "_id": str(request.app.database["users"].find_one({"username": username})["_id"])}
        encoded = jwtEncoder(obj)
        mailSender(encoded)
        return FileResponse("mail-sent.html")
    else:
        return FileResponse("mail-sent.html")
    

@router.get("/")
async def pageLoader():
    return FileResponse("get_username.html")
