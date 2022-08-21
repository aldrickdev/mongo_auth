from pydantic import BaseModel, Field, EmailStr


class UserDetails(BaseModel):
    username: str = Field(min_length=8, max_length=50)
    email: EmailStr
    disabled: bool
    role: str


class UserLoginUsername(BaseModel):
    username: str = Field(min_length=8, max_length=50)
    password: str


class User(UserDetails):
    hashed_password: str
    date_created: str


class UserCreate(UserDetails):
    password: str
