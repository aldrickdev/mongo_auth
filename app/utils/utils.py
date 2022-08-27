# standard imports
from typing import Optional
from datetime import datetime, timedelta

# third party imports
from jose import JWTError, jwt
from passlib.context import CryptContext

# user imports
import models
import exceptions
from routes.user import res_req_models

# context used for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def hash_password(password: str) -> str:
    """Returns the hashed password"""

    # hashes the password
    return pwd_context.hash(password)


# TODO: maybe break this function up into a password validator and get user from username
async def validate_credentials(username: str, password: str) -> Optional[models.User]:
    """Return a valid user if they exist"""

    # find the user in the database by username, return None
    # user_found = await user_db.find_one(user_db.username == username)
    user_found = await models.get_user_from_username(username)

    if user_found is None:
        return None

    # verify the password and the hashed password
    if not pwd_context.verify(password, user_found.hashed_password):
        raise exceptions.InvalidCredentialsError("Incorrect Password")

    else:
        return user_found


async def create_token(username: str, expires_in: int, secret: str, algorithm: str) -> str:
    """Returns a JWT"""

    # create the data to be encoded
    try:
        access_token_expires = timedelta(minutes=int(expires_in))

    except ValueError:
        raise ValueError("Time to expire not integer")

    data_to_encode = {"sub": username, "exp": datetime.utcnow() + access_token_expires}

    # create the access token
    try:
        return jwt.encode(data_to_encode, secret, algorithm=algorithm)

    except JWTError:
        raise JWTError("Error Creating a JWT")


async def get_username_from_jwt(
    token: res_req_models.TokenData, secret: str, algorithm: str
) -> Optional[str]:
    """Return the username of the user in the token"""

    try:
        # decode the JWT
        payload = jwt.decode(token, secret, algorithms=algorithm)

    except JWTError:
        raise JWTError("Something went wrong when decoding the token")

    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("The signature has expired")

    except jwt.JWTClaimsError:
        raise jwt.JWTClaimsError("Claim was invalid")

    # return the username, if it doesn't exist return None
    username: str = payload.get("sub")

    if username is None:
        return None

    return username
