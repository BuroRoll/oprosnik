from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = ''
    SECRET_KEY: str = 'secret_key'


settings = Settings()
