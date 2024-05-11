from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


load_dotenv()


class RedisSettings(BaseSettings):
    host: str = ...
    port: int = ...

    model_config = SettingsConfigDict(env_prefix='redis_')


class APPSettings(BaseSettings):
    project_name: str = 'Notifications API'
    redis: RedisSettings = RedisSettings()


settings = APPSettings()
