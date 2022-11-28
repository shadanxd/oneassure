import os
import uvicorn
from fastapi import Depends
from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from auth import AuthHandler
from database import DBHandler
import usermodels
from dotenv import load_dotenv

app = FastAPI()


oauth2_schema = OAuth2PasswordBearer(tokenUrl = "/login")
load_dotenv()
collection_name_env = os.getenv('user_type')
collection = f'OneAssure{collection_name_env}'


@app.post('/signup/')
async def signup(user: usermodels.UserBase):
    collection_name = f'OneAssure{user.type}'
    scope = {"_id": 0}
    cursor = await DBHandler.fetch({"username": user.username}, collection_name, scope)
    if len(list(cursor)) > 0:
        return HTTPException(status_code = 400, detail = "Username already exists")
    await DBHandler.save([user.dict()], collection_name)
    return user


@app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    scope = {"_id": 0}
    cursor = await DBHandler.fetch({"username": username}, collection, scope)
    user_list = list(cursor)
    if len(user_list) == 0:
        raise HTTPException(status_code = 401, detail = "Invalid Username")
    else:
        if AuthHandler.verify_password(password, user_list[0]['password']):
            return {"access_token": AuthHandler.encode_token(username)}
        else:
            raise HTTPException(status_code = 401, detail = "Incorrect Password")


@app.put('/update/')
async def update(user: usermodels.UserUpdate, token: str = Depends(oauth2_schema)):
    payload: dict = AuthHandler.decode_token(token)
    if payload['sub'] == user.username:
        await DBHandler.update({"username": user.username}, user.dict(exclude_none= True), collection)
        return {"status": "details updated"}
    else:
        return HTTPException(status_code = 401, detail = 'Invalid Token')


@app.get('/getDetails/{username}')
async def getDetails(username: str, token: str = Depends(oauth2_schema)):
    payload: dict = AuthHandler.decode_token(token)
    excluded_fields = {"_id": 0, "type": 0, "password": 0}
    if payload['sub'] == username:
        cursor = await DBHandler.fetch({"username": username}, collection, excluded_fields)
        return list(cursor)[0]
    else:
        return HTTPException(status_code = 401, detail = 'Invalid Token')


@app.delete('/delete/{username}')
async def deleteUser(username: str, token: str = Depends(oauth2_schema)):
    payload: dict = AuthHandler.decode_token(token)
    if payload['sub'] == username:
        await DBHandler.delete({"username": username}, collection)
        return {"Deleting user": "success"}
    else:
        return HTTPException(status_code = 401, detail = 'Invalid Token')

if __name__ == "__main__":
    uvicorn.run(app)
