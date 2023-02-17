from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.middleware.auth import ACCESS_TOKEN_EXPIRE_MINUTES, get_current_active_user, authenticate_user, \
    create_access_token
from app.sql_app.schemas.schemas import Token, UserModel
from app.sql_app.crud.auth import UserDao
router = APIRouter(prefix="/users", )


@router.get("/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/me", tags=["users"])
async def read_user_me():
    return {"username": "fake_current_user"}


@router.get("/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}


@router.post("/register")
async def register(user: UserModel):
    print(user)
    if UserDao.register_user(*user):
        return {"msg": "注册成功", "data": user}
    else:
        return {"msg": "注册失败"}


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserModel)
async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: UserModel = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
