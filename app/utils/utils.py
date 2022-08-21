# third party imports
from jose import JWTError, jwt


async def get_username_from_token(token: str, secret_key: str, algo: str) -> str | None:
    try:
        print(f"Decoding token: {token}")
        payload = jwt.decode(
            token=token,
            key=secret_key,
            algorithms=algo,
        )

    except JWTError:
        print("Error decoding token")
        return None

    print("Extracting username from the payload")

    return payload.get("sub")
