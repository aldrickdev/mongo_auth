# standard imports
import os

# third party imports
from fastapi import FastAPI

# user imports
import database
import models
import env_vars
import routes


env_vars.init_env_vars()


# creates a FastAPI instance
app = FastAPI(
    title="Mongo auth",
    version="0.0.1",
    openapi_tags=[
        {
            "name": "User",
            "Description": "Operations that can be user to interact with the User database",
        },
    ],
)

app.include_router(routes.user_router)


@app.on_event("startup")
async def server_startup() -> None:
    # get mongo_db credentials
    mongo_user: str | None = os.environ.get("MONGO_USER")
    mongo_pwd: str | None = os.environ.get("MONGO_PWD")

    # get database models
    mongo_models = [models.User]

    # if isinstance(mongo_user, str) and isinstance(mongo_pwd, str):
        # await database.init_db(mongo_user, mongo_pwd, mongo_models)

    print("Connected to Database")
