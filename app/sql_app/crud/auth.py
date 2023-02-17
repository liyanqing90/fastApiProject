from app.sql_app.database import get_db_session
from app.sql_app.models.user import User
from app.sql_app.schemas.schemas import UserInDB
from sqlalchemy.orm import Session

def get_user_by_username(db, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db, email: str):
    return db.query(User).filter(User.email == email).first()


# 模拟数据库，存储用户信息
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


# 根据用户名获取用户信息
def get_user(username: str):
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)

def get_users(db: Session):
    return db.query(User).all()
class UserDao:
    @staticmethod
    def register_user(username, email, password, ):
        try:
            print(username)
            with get_db_session() as db:
                users = get_users(db)
                if db:
                    raise Exception("邮箱已注册")
                pwd = password
                user = User(username, pwd, email)
                print("123")
                db.session.add(user)
                db.session.commit()
        except:
            raise "注册失败"
        return "Success"
