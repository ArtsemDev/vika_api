from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.models import User
from core.schemas import RegisterSchema, LoginSchema, UserDBSchema

auth = APIRouter()


@auth.post('/register', response_model=UserDBSchema, response_model_exclude={'hashed_password', 'password'})
async def register(user: RegisterSchema):
    user = UserDBSchema(**user.dict())
    obj = User(**user.dict(exclude={'password', 'id'}))
    try:
        await obj.save()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='email is not unique')
    else:
        user.id = obj.id
        return user


@auth.post('/login', response_model=UserDBSchema, response_model_exclude={'hashed_password', 'password'})
async def login(user: LoginSchema):
    obj = await User.scalars(select(User).filter(User.email == user.email))
    if obj:
        try:
            user_schema = UserDBSchema(**obj[0].dict() | {'password': user.password})
        except ValidationError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='password is invalid')
        else:
            return user_schema
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')