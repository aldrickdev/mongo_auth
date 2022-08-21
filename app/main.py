# standard
from datetime import datetime, timedelta
import os

# third party
from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt

# user
import models
import utils
import env

database: list[models.User] = []

# tells your endpoints where to go to get a token if a valid token wasn't already
# provided by the client
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/token")

env.init_env_vars()


app = FastAPI(
    title="Mongo auth",
    version="0.0.1",
    openapi_tags=[
        {
            "name": "Users",
            "Description": "Operations that can be user to interact with the User database",
        },
        {"name": "Token", "Description": "Endpoint to get a token"},
    ],
)


@app.post(
    path="/api/v1/user/create",
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
    response_model=models.UserDetails,
)
async def add_user(provided_user: models.UserCreate) -> models.UserDetails:
    now = datetime.utcnow()

    new_user_dict = provided_user.dict()
    new_user_dict["hashed_password"] = f"hashed {provided_user.password}"
    new_user_dict["date_created"] = str(now)

    new_user = models.User(**new_user_dict)

    database.append(new_user)

    return models.UserDetails(**new_user.dict())


@app.get(
    path="/api/v1/user/details",
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    response_model=models.UserDetails,
)
async def get_user_details(token: str = Depends(oauth2_scheme)) -> models.UserDetails:
    # find the user based on the token provided
    username = await utils.get_username_from_token(
        token,
        os.environ.get("SECRET_KEY"),
        os.environ.get("ALGORITHM"),
    )

    # check to see if the payload had a username
    if username is None:
        print("No username found in the payload")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username not found in the token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print(f"Looking for {username} in the database")

    # check to see if the user is in the database
    db_user = None
    for user in database:
        if user.username == username:
            db_user = user
            print("User found")
            break

    # user wasn't found in the database
    if db_user is None:
        print("User wasn't found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User wasn't found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return models.UserDetails(**db_user.dict())


@app.put(
    path="/api/v1/user/edit",
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    response_model=models.UserDetails,
)
async def edit_user(
    update: dict, token: str = Depends(oauth2_scheme)
) -> models.UserDetails:
    # find the user based on the token provided
    username = await utils.get_username_from_token(
        token,
        os.environ.get("SECRET_KEY"),
        os.environ.get("ALGORITHM"),
    )

    # check to see if the payload had a username
    if username is None:
        print("No username found in the payload")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username not found in the token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print(f"Looking for {username} in the database")

    # check to see if the user is in the database
    db_user = None
    for user in database:
        if user.username == username:
            db_user = user
            print("User found")
            break

    # user wasn't found in the database
    if db_user is None:
        print("User wasn't found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User wasn't found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print(f"Fields to update: {update}")
    # update the users info locally
    current_user_details = db_user.dict()

    for field in update.items():
        current_user_details[field[0]] = field[1]

    print(f"Users new details: {current_user_details}")

    # update the user in the database
    for user in database:
        if user.username == db_user.username:
            # update the user in the database
            if "username" in current_user_details:
                user.username = current_user_details["username"]

    return models.UserDetails(**current_user_details)


@app.post(
    path="/api/v1/user/token",
    status_code=status.HTTP_200_OK,
    tags=["Users"],
    response_model=models.Token,
)
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()) -> models.Token:
    # Extract the username and password
    username: str = form_data.username
    password: str = form_data.password

    # setting default value
    db_user = None

    print(f"Username: {username}")
    print(f"Password: {password}")

    # look for user in the database
    print("Looking for user")
    for user in database:
        if user.username == username:
            db_user = user
            print("User found")
            break

    # check if the user wasn't found in the Database
    if db_user is None:
        print("User was not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User was not found in the database",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # User was found so lets create a token for them
    expires = datetime.utcnow() + timedelta(minutes=5)

    # dict with the data that we want to encode
    data_to_encode = {"sub": db_user.username, "exp": expires}

    # encode the data and create a jwt
    encoded_token = jwt.encode(
        claims=data_to_encode,
        key=os.environ.get("SECRET_KEY"),
        algorithm=os.envirion.get("ALGORITHM"),
    )

    print(encoded_token)

    return models.Token(access_token=encoded_token, token_type="bearer")
