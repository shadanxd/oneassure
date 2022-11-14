import random
import string
from typing import Optional
import uvicorn
from fastapi import Depends
from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from auth import AuthHandler
from database import Data

app = FastAPI()


class User(BaseModel):
    username: str = "John_Doe"
    name: str = "john123"
    phone: int = "1234"
    password: str = "john@123"
    description: Optional[str] = None


@app.put('/signup/')
async def signup(user: User):
    item = {"_id": user.username, "name": user.name, "phone": user.phone,
            "password": AuthHandler.get_password_hash(user.password), "description": user.description,
            "Key": generate_random()}
    await Data.save(item)
    return user


def generate_random():
    x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6))
    return x


@app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    user = Data(username)
    hashed_password = await user.user_query()
    if hashed_password and AuthHandler.verify_password(password, hashed_password):
        return AuthHandler.encode_token(username)
    else:
        return {"Password/Username": "Incorrect"}


@app.post('/login/update/phone/{username}/{number}')
async def update(username: str, number: int, payload: dict = Depends(AuthHandler.decode_token)):
    if payload['sub'] == username:
        await Data(payload['sub']).update_phone(number)
    else:
        return HTTPException(status_code = 401, detail = 'Invalid Token')


@app.post('/login/update/name/{username}/{new_name}')
async def name_update(username: str, new_name: str, payload: dict = Depends(AuthHandler.decode_token)):
    if payload['sub'] == username:
        await Data(payload['sub']).name_update(new_name)
    else:
        return HTTPException(status_code = 401, detail = 'Invalid Token')


@app.get('/login/getDetails/{username}')
async def getDetails(username: str, payload: dict = Depends(AuthHandler.decode_token)):
    if payload['sub'] == username:
        return await Data(payload['sub']).getUserDetails()
    else:
        return HTTPException(status_code = 401, detail = 'Invalid Token')


if __name__ == "__main__":
    uvicorn.run(app)
