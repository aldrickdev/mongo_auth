# standard imports
from typing import Optional

# third party imports
import pydantic

# user imports


class UserDetails(pydantic.BaseModel):
    """The model that represents what basic user details are"""

    username: str = pydantic.Field(min_length=8, max_length=30)
    email: pydantic.EmailStr
    disabled: bool
    role: str


class UserLoginUsername(pydantic.BaseModel):
    """The model that represents what is expected from the user when logging in with username"""

    username: str = pydantic.Field(min_length=8, max_length=30)
    password: str


class UserCreate(UserDetails):
    """The model that represents what is expected from the user during user creation"""

    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "aldrickcastro",
                "email": "aldrick@greymint.com",
                "disabled": False,
                "role": "standard",
                "password": "p@ssword",
            }
        }


class UserUpdate(pydantic.BaseModel):
    email: Optional[pydantic.EmailStr] = None
    role: Optional[str] = None
    password: Optional[str] = None


class Token(pydantic.BaseModel):
    """Model of a token"""

    access_token: str
    token_type: str


class TokenData(pydantic.BaseModel):
    """Model of a decoded token"""

    username: str | None = None
