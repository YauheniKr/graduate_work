from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool

    class Config:
        env_prefix = 'PAYGATEWAY_'


settings = Settings()
