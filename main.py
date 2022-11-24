import uvicorn
from fastapi import Depends
from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from auth import AuthHandler
from database import DBHandler
import usermodels

app = FastAPI()


oauth2_schema = OAuth2PasswordBearer(tokenUrl = "/login")


@app.post('/signup/')
async def signup(user: usermodels.UserBase):
    if await DBHandler.getUserDetails(user.username) is not None:
        return HTTPException(status_code = 400, detail = "Username already exists")
    await DBHandler.save(user.dict())
    return user


@app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    user = await DBHandler.getUserDetails(username)
    if user is None:
        raise HTTPException(status_code = 401, detail = "Invalid Username")
    else:
        if AuthHandler.verify_password(password, user['password']):
            return {"access_token": AuthHandler.encode_token(username)}
        else:
            raise HTTPException(status_code = 401, detail = "Incorrect Password")


@app.put('/update/phone/{username}/{number}')
async def update(username: str, number: int, token: str = Depends(oauth2_schema)):
    payload: dict = AuthHandler.decode_token(token)
    if payload['sub'] == username:
        scope = {"username": username, "new_number": number}
        await DBHandler.update_user_details(scope)
        return {"status": "phone number updated"}
    else:
        return HTTPException(status_code = 401, detail = 'Invalid Token')


@app.put('/update/name/{username}/{new_name}')
async def name_update(username: str, new_name: str, token: str = Depends(oauth2_schema)):
    payload: dict = AuthHandler.decode_token(token)
    if payload['sub'] == username:
        scope = {"username": username, "new_name": new_name}
        await DBHandler.update_user_details(scope)
        return {"status": "name updated"}
    else:
        return HTTPException(status_code = 401, detail = 'Invalid Token')


@app.get('/getDetails/{username}')
async def getDetails(username: str, token: str = Depends(oauth2_schema)):
    payload: dict = AuthHandler.decode_token(token)
    if payload['sub'] == username:
        user = await DBHandler.getUserDetails(username)
        return user
    else:
        return HTTPException(status_code = 401, detail = 'Invalid Token')


if __name__ == "__main__":
    uvicorn.run(app)
