# standard imports
import os
from datetime import datetime

# third party imports
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

# user imports
import models
import utils
import exceptions
from routes.user import res_req_models

# tells your endpoints where to go to get a token if a valid token wasn't already
# provided by the client
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/token")


# create router instance
user_router = APIRouter(
    prefix="/api/v1/user",
    tags=["User"],
)


@user_router.post(
    path="/create",
    status_code=status.HTTP_201_CREATED,
    response_model=res_req_models.UserDetails,
)
async def add_user(provided_user: res_req_models.UserCreate) -> res_req_models.UserDetails:
    """Endpoint to create a user"""
    # check if the user already exist in the database, if so raise error
    user = await models.User.find_one(models.User.username == provided_user.username)

    if user is not None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User Already Exist")

    # hash the password that the user has provided
    hashed_password = await utils.hash_password(provided_user.password)

    # create the user model to be added to the database
    new_user = models.User(
        hashed_password=hashed_password, date_created=str(datetime.utcnow()), **provided_user.dict()
    )

    # add the user to the database
    await new_user.insert()

    # return the users details
    return res_req_models.UserDetails(**new_user.dict())


@user_router.post(
    path="/token", status_code=status.HTTP_200_OK, response_model=res_req_models.Token
)
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()) -> res_req_models.Token:
    """Endpoint to get a token for a user"""

    # extract the username and password from the form
    username = form_data.username
    password = form_data.password

    # get variables for creating the token
    expires_in = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
    secret = os.environ.get("SECRET_KEY")
    algorithm = os.environ.get("ALGORITHM")

    if expires_in is None or secret is None or algorithm is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Missing Environment Variables",
        )

    # check to see if the user exist in the database, if not raise
    user = await utils.validate_credentials(username, password)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    else:
        # user exist and valid password was entered, create and return a token
        try:
            token = await utils.create_token(user.username, expires_in, secret, algorithm)

            print(f"{token = }")

        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error with expire in environment variable",
            )

        return res_req_models.Token(access_token=token, token_type="bearer")


@user_router.get(
    path="/details", status_code=status.HTTP_200_OK, response_model=res_req_models.UserDetails
)
async def get_user_details(token: str = Depends(oauth2_scheme)) -> res_req_models.UserDetails:
    """Endpoint to get user information"""

    # get variables for creating the token
    secret = os.environ.get("SECRET_KEY")
    algorithm = os.environ.get("ALGORITHM")

    if secret is None or algorithm is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Missing Environment Variables",
        )

    # get the user from JWT
    username = await utils.get_username_from_jwt(token, secret, algorithm)
    user = await models.get_user_from_username(username)

    # if the user is available, return the user details
    if user is None:
        raise exceptions.UserNotFoundError("User was not found")

    return res_req_models.UserDetails(**user.dict())


@user_router.put(
    path="/edit", status_code=status.HTTP_202_ACCEPTED, response_model=res_req_models.UserDetails
)
async def update_user(
    to_update: res_req_models.UserUpdate, token: str = Depends(oauth2_scheme)
) -> res_req_models.UserDetails:
    """Endpoint used to update a users information"""

    # get the user from jwt
    # get variables for creating the token
    secret = os.environ.get("SECRET_KEY")
    algorithm = os.environ.get("ALGORITHM")

    if secret is None or algorithm is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Missing Environment Variables",
        )

    # get the user from JWT
    username = await utils.get_username_from_jwt(token, secret, algorithm)
    user = await models.get_user_from_username(username)

    # if the user is available, return the user details
    if user is None:
        raise exceptions.UserNotFoundError("User was not found")

    # update the fields
    set_command = {}

    for k, v in to_update.dict().items():
        if v is not None:
            set_command[k] = v

    await user.update({"$set": set_command})

    # return the user details
    return res_req_models.UserDetails(**user.dict())


@user_router.put(
    path="/disable", status_code=status.HTTP_202_ACCEPTED, response_model=res_req_models.UserDetails
)
async def disable_user(token: str = Depends(oauth2_scheme)) -> res_req_models.UserDetails:
    """Endpoint used to update a users information"""

    # get the user from jwt
    # get variables for creating the token
    secret = os.environ.get("SECRET_KEY")
    algorithm = os.environ.get("ALGORITHM")

    if secret is None or algorithm is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Missing Environment Variables",
        )

    # get the user from JWT
    username = await utils.get_username_from_jwt(token, secret, algorithm)
    user = await models.get_user_from_username(username)

    # if the user is available, return the user details
    if user is None:
        raise exceptions.UserNotFoundError("User was not found")

    # update the disabled field to true
    await user.update({"$set": {"disabled": True}})

    # return the user details
    return res_req_models.UserDetails(**user.dict())
