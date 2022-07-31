from pydantic import BaseModel
import datetime as dt


class RegisterUserRequest(BaseModel):
    name: str
    surname: str
    age: int


class UserModel(BaseModel):
    id: int
    name: str
    surname: str
    age: int

    class Config:
        orm_mode = True


class ItemPicnic(BaseModel):
    city_id: int
    time: dt.datetime


class ItemRegistration(BaseModel):
    user_id: int
    picnic_id: int


class ItemCity(BaseModel):
    city: str