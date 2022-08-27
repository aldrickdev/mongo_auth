import os


def init_env_vars() -> None:
    env = os.environ.get("ENV")

    if env is None:
        print("Running in Local Environment")
        from dotenv import load_dotenv, find_dotenv

        env_file_location = find_dotenv()

        if not env_file_location:
            raise FileNotFoundError("Running Locally with no .env file")

        load_dotenv(env_file_location)
        print(f"{env_file_location} has been loaded")

        return

    print(f"Running in {env}")
