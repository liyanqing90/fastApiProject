from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://yourusername:yourpassword@localhost/yourdatabase"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Liyanqing123456.@127.0.0.1:3306/demo"

engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=QueuePool, pool_size=5, max_overflow=0)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 注释链接池使用方式
# class Item(Base):
#     __tablename__ = "items"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(50), index=True)
#
#
# @app.get("/items/")
# async def read_items(db: Session = Depends(get_db)):
#     return db.query(Item).all()

def create_table():
    Base.metadata.create_all(bind=engine)
