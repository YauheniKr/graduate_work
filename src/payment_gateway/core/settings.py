from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool
    sqlalchemy_uri: str
    rabbitmq_uri: str
    rabbitmq_queue: str

    class Config:
        env_prefix = 'PAYGATEWAY_'


settings = Settings()