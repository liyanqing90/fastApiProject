from datetime import datetime

from sqlalchemy.orm import Session

from app.sql_app.models.user import User
from app.sql_app.schemas.schemas import UserCreate, UserLogin


def get_user_by_username(db, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db, email: str):
    return db.query(User).filter(User.email == email).first()


def model_to_dict(model):
    return {key: getattr(model, key) for key in model.__table__.columns.keys()}


class SSO:
    def __init__(self, db: Session, ):
        self.db = db

    def create_user(self, user: UserCreate):
        if self.db.query(User).filter(email=user.email).first():
            return {"code": "10001"}
        db_user = User(username=user.username, email=user.email, password=user.password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return {"code": "00000"}

    def login(self, user: UserLogin):
        try:
            if not (user := self.db.query(User).filter(User.email == user.email).first()):
                return {"code": "10001"}
            if user.password != user.password:
                return {"code": "10002"}
            else:
                user.last_login_at = datetime.now()
                self.db.commit()
                data = model_to_dict(user)
                return {"code": "00000", "data": data}
        except Exception as e:
            print(e)
            return {"code": "90009"}
