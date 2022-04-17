from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool
    sqlalchemy_uri: str
    rabbitmq_uri: str
    rabbitmq_queue: str
    app_info: str
    app_version: str
    api_key: str
    api_webhook_key: str
    app_url: str
    account: str

    class Config:
        env_prefix = 'PAYGATEWAY_'
        case_sentive = False


settings = Settings()
