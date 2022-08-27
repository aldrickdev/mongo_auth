# standard imports
from typing import Optional

# third party imports
import pydantic

# user imports
import beanie


class User(beanie.Document):
    """The model the represents the User in the database"""

    username: str = pydantic.Field(min_length=8, max_length=30)
    email: pydantic.EmailStr
    disabled: Optional[bool] = False
    role: Optional[str] = "standard"
    hashed_password: str
    date_created: str  # TODO: make this be filled in when the user is created automatically

    class Settings:
        name = "Users"


async def get_user_from_username(username: str) -> Optional[User]:
    """returns a user if one is found, otherwise return None"""

    return await User.find_one(User.username == username)
