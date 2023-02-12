import datetime
import os
import zipfile

import jwt
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from starlette.responses import FileResponse

load_dotenv()
app = FastAPI()
SECRET_KEY = os.getenv("SECRET")


@app.get("/")
async def root():
    secret_key = os.getenv("SECRET_KEY")
    return {"message": f"Your secret key is: {secret_key}"}


def check_token(token: str):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True
    except jwt.exceptions.InvalidTokenError:
        return False


@app.post("/hello")
async def hello(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=400, detail="Authorization header is missing")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Authorization header must start with 'Bearer '")
    token = authorization.split(" ")[1]
    if not check_token(token):
        raise HTTPException(status_code=401, detail="Invalid access token")

    return {"message": "Hello, World!"}


@app.post("/generate-token")
async def generate_token(x_forwarded_for: str = Header(None)):
    expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    payload = {
        "exp": expiry,
        "nbf": datetime.datetime.utcnow(),
        "iat": datetime.datetime.utcnow(),
        "iss": x_forwarded_for,
    }

    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return {"access_token": jwt_token}


@app.get('/zip')
async def get_zip():
    with zipfile.ZipFile("files.zip", "w") as zip_obj:
        zip_obj.write(f"files/zipMePlease.txt")

    return FileResponse("files.zip", media_type="application/zip")
