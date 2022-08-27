from typing import Optional
import asyncio
import os

import motor.motor_asyncio
import beanie
from pydantic import Field, EmailStr

import env_vars

env_vars.init_env_vars()


class User(beanie.Document):
    username: str = Field(min_length=8, max_length=50)
    email: EmailStr
    disabled: Optional[bool] = False
    role: Optional[str] = "standard"
    hashed_password: str
    date_created: Optional[str] = ""

    def to_json(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "disabled": self.disabled,
            "role": self.role,
            "hashed_password": self.hashed_password,
            "date_created": self.date_created,
        }


async def test():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        f"mongodb://{os.environ.get('MONGO_USER')}:{os.environ.get('MONGO_PWD')}@mongo:27017"
    )

    await beanie.init_beanie(database=client.greymintauth, document_models=[User])

    # Creating a test user
    test_user = User(
        username="aldrickcastro",
        email="ajkasbd@gmail.com",
        hashed_password="kaknjsdf",
    )

    await test_user.insert()

    all_users = await User.find_all().to_list()
    for user in all_users:
        print(user.to_json())


asyncio.run(test())
