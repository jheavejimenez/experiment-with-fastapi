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


@app.post("/hello")
async def hello(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=400, detail="Authorization header is required")

    if not authorization.startswith("Bearer"):
        raise HTTPException(status_code=400, detail="Authorization header must start with 'Bearer'")

    # Extract the JWT token from the authorization header
    token = authorization.split(" ")[1]

    try:
        jwt.decode(token, str(SECRET_KEY), algorithms=["HS256"])
    except jwt.exceptions.InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid JWT signature")
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="JWT has expired")

    return {"message": "Hello World"}


@app.post("/generate-token")
async def generate_token(x_forwarded_for: str = Header(None)):
    expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    payload = {
        "exp": expiry,
        "nbf": datetime.datetime.utcnow(),
        "iat": datetime.datetime.utcnow(),
        "iss": x_forwarded_for,
    }

    jwt_token = jwt.encode(payload, str(SECRET_KEY), algorithm="HS256")
    return {"access_token": jwt_token}


@app.get('/zip')
async def get_zip():
    folder_path = 'zip_files/files.zip'
    file_name = "files/zipMePlease.txt"

    with zipfile.ZipFile(folder_path, "w") as zip_obj:
        zip_obj.write(file_name)

    return FileResponse(folder_path, media_type="application/zip")
