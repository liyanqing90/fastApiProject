from fastapi import Query
from pydantic import BaseModel


# 定义令牌模型
class Token(BaseModel):
    access_token: str
    token_type: str


# 定义令牌数据模型
class TokenData(BaseModel):
    username: str | None


# 定义用户模型
class UserModel(BaseModel):
    username: str
    email: str
    password: str = Query(min_length=6, max_length=20, description="请输入6-20位字符")


# 继承自用户模型，添加散列密码字段
class UserInDB(UserModel):
    hashed_password: str
