from typing import Optional
import uvicorn
from fastapi import Depends
from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from auth import AuthHandler
from database import DBHandler

app = FastAPI()


class User(BaseModel):
    username: str = "John_Doe"
    name: str = "john123"
    phone: int = "1234"
    password: str = "john@123"
    description: Optional[str] = None


@app.put('/signup/')
async def signup(user: User):
    item = {"username": user.username, "name": user.name, "phone": user.phone,
            "password": AuthHandler.get_password_hash(user.password), "description": user.description}
    await DBHandler.save(item)
    return user


@app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    user = await DBHandler.getUserDetails(username)
    if user is None:
        return {"username/password": "Invalid"}
    elif username == user['username'] and AuthHandler.verify_password(password, user['password']):
        return {AuthHandler.encode_token(username)}


@app.post('/login/update/phone/{username}/{number}')
async def update(username: str, number: int, payload: dict = Depends(AuthHandler.decode_token)):
    if payload['sub'] == username:
        scope = {"username": username, "new_number": number}
        await DBHandler.update_user_details(scope)
        return {"status": "phone number updated"}
    else:
        return HTTPException(status_code = 401, detail = 'Invalid Token')


@app.post('/login/update/name/{username}/{new_name}')
async def name_update(username: str, new_name: str, payload: dict = Depends(AuthHandler.decode_token)):
    if payload['sub'] == username:
        scope = {"username": username, "new_name": new_name}
        await DBHandler.update_user_details(scope)
        return {"status": "name updated"}
    else:
        return HTTPException(status_code = 401, detail = 'Invalid Token')


@app.get('/login/getDetails/{username}')
async def getDetails(username: str, payload: dict = Depends(AuthHandler.decode_token)):
    if payload['sub'] == username:
        user = await DBHandler.getUserDetails(username)
        return user
    else:
        return HTTPException(status_code = 401, detail = 'Invalid Token')


if __name__ == "__main__":
    uvicorn.run(app)
