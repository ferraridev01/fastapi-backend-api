import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    def __init__(self):
        if not self.SECRET_KEY:
            raise ValueError(
                "SECRET_KEY variable is missing in the environment configuration"
            )


settings = Settings()
