from enum import Enum
from typing import Union, Set

from fastapi import FastAPI, Query, Path, Body, Cookie,Header
from pydantic import BaseModel, Field, HttpUrl,EmailStr

app = FastAPI()
debug = True
from uuid import UUID


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str = Field(max_length=3)
    description: str = None
    price: float
    is_offer: Union[bool, None] = None
    tax: Union[float, None] = None
    tags: Set[str] = set()
    image: Union[Image, None] = None
    id: UUID = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/me")
async def say_hello(user_agent: Union[str, None] = Header(default=None)):
    return {"message": f"Hello My friend", "ads_id": user_agent}


@app.get("/hello/{name}")
async def say_hello(name: str = Query(min_length=2)):
    return {"message": f"Hello {name}"}


@app.put("/items/{item_id}")
async def update_item(
        *,
        item_id: int = Path(title="The ID of the item to get", ge=100),
        item: Item
):
    return {"item_name": item.name, "item_id": item_id}


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item = Body(embed=True)):
    print("123")
    print(item_id)
    item_dict = item.dict()
    print(item_dict)
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Union[str, None] = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved