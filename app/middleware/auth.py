from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.sql_app.crud.auth import get_user_by_username
from app.sql_app.database import get_db
from app.sql_app.schemas.schemas import TokenData, UserCreate

# 生成密钥的命令：openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 创建密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 创建 OAuth2PasswordBearer 实例，用于获取令牌
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 创建 FastAPI 实例
app = FastAPI()


# 校验密码
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# 生成密码散列值
def get_password_hash(password):
    return pwd_context.hash(password)


# 验证用户身份
def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# 创建访问令牌
def create_access_token(data: dict, expires_delta: timedelta | None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 获取当前用户
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserCreate = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
