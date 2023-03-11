from pydantic import BaseModel, Field, EmailStr, root_validator, validator

from core.settings import PWD_CONTEXT


class RegisterSchema(BaseModel):
    email: EmailStr = Field(
        title='User Email',
        default='Unique User Email',
    )
    username: str = Field(
        title='Username',
        description='Username',
        max_length=128,
    )
    password: str = Field(
        title='User Password',
        description='User Password',
        min_length=8,
        max_length=64,
        regex=r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})'
    )
    repeat_password: str = Field(
        title='Repeat Password',
        description='Repeat Password',
        min_length=8,
        max_length=64,
        regex=r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})'
    )

    @root_validator
    def validator(cls, values: dict) -> dict:
        if values.get('password') != values.get('repeat_password'):
            raise ValueError("passwords don't match")

        if values.get('username').lower() in values.get('password').lower():
            raise ValueError('the password must not contain the username')

        if values.get('email').lower().split('@')[0] in values.get('password').lower():
            raise ValueError('the password must not contain the email')

        return values


class LoginSchema(BaseModel):
    email: EmailStr = Field(
        title='User Email',
        default='Unique User Email',
    )
    password: str = Field(
        title='User Password',
        description='User Password',
        min_length=8,
        max_length=64,
        regex=r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})'
    )


class UserDBSchema(BaseModel):
    id: int = Field(
        ge=1,
        title='User Unique ID',
        description='User Unique ID',
        default=None
    )
    email: str = Field(
        title='User Email',
        default='Unique User Email',
    )
    username: str = Field(
        title='Username',
        description='Username',
        max_length=128,
    )
    hashed_password: str = Field(
        title='User Hashed Password',
        description='User Hashed Password',
        min_length=8,
        max_length=512,
        default=None,
    )
    password: str = Field(
        title='User Password',
        description='User Password',
        min_length=8,
        max_length=64,
        regex=r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})',
        default=None
    )

    @root_validator(pre=True)
    def validator(cls, values: dict) -> dict:
        if values.get('password') and not values.get('hashed_password'):
            values['hashed_password'] = PWD_CONTEXT.hash(values.get('password'))
        elif values.get('password') and values.get('hashed_password'):
            if not PWD_CONTEXT.verify(values.get('password'), values.get('hashed_password')):
                raise ValueError('password is invalid')
        return values

    class Config:
        orm_mode = True
