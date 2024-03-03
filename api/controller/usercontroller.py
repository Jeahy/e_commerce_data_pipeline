#Controllers act as the bridge between incoming requests and your application’s
# core logic, providing a structured way to handle routes and endpoints. 
import sys
import os
sys.path.append(os.path.abspath('/home/pkn/ecompipeline/api'))

from fastapi import HTTPException, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
from service.userservice import UserService
from dto.user import User
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from dto.customresponsemessage import CustomResponseMessage

user_controller_router = InferringRouter()

@cbv(user_controller_router) #Class based views: allowing the router to automatically infer route paths and HTTP methods from method names within the class
class UserController:
    def __init__(self): 
        self.userService = UserService()

    @user_controller_router.post("/register")
    def register(self, user: User):
        try:
            usr = self.userService.register(user)
            if usr is not False:
                return CustomResponseMessage(status_code = 200, message = f"User {user.username} registered successfully.")
            else:
                raise HTTPException(status_code=422, detail="User already exists")
        except Exception as e:
            raise HTTPException(status_code=e.status_code, detail=str(e.detail))

    @user_controller_router.post("/token")
    def get_access_token(self, form_data: OAuth2PasswordRequestForm = Depends()):
        try:
            access_token = self.userService.get_access_token(form_data)
            if access_token["access_token"] is None:
                raise HTTPException(status_code=400, detail="Incorrect username or password")
            return access_token
        except Exception as e:
            raise HTTPException(status_code=e.status_code, detail=str(e.detail))

    @user_controller_router.post("/logout")
    def logout(self, token: str = Header(None)):
        try:
            if token is None: 
                raise HTTPException(status_code=401, detail="Invalid token")
            self.userService.logout(token)
            return CustomResponseMessage(status_code = 200, message = "Logged out successfully")
        except Exception as e:
            raise HTTPException(status_code=e.status_code, detail=str(e.detail))