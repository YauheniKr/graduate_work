from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool
    sqlalchemy_uri: str

    class Config:
        env_prefix = 'PAYGATEWAY_'


settings = Settings()
