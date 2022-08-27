# standard imports

# third party imports
import pydantic

# user imports


class Token(pydantic.BaseModel):
    """Models of atoken"""

    access_token: str
    token_type: str


class TokenData(pydantic.BaseModel):
    username: str | None = None
