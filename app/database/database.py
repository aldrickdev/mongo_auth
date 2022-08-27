# standard imports
from typing import Any

# third party imports
import motor.motor_asyncio
import beanie

# user imports


async def init_db(mongo_user: str, mongo_pwd: str, models: list[Any]) -> None:
    """Function that will initialize the MongoDB Database"""

    # create the connection string for the database
    connection: str = f"mongodb://{mongo_user}:{mongo_pwd}@mongo:27017"

    # create the a async client with the connection string
    client = motor.motor_asyncio.AsyncIOMotorClient(connection)

    # initializes the connection to the database, database is called greymintauth
    await beanie.init_beanie(database=client.greymintauth, document_models=models)
