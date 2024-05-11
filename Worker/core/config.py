from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


load_dotenv()


class MongoSettings(BaseSettings):
    name: str = ...
    host: str = ...
    port: int = ...
    model_config: str = SettingsConfigDict(env_prefix='notifications_mongo_db_')

    @property
    def uri(self):
        return f"mongodb://{self.host}:{self.port}/"


class AuthSettings(BaseSettings):
    secret_key: str = ...
    jwt_algorithm: str = ...
    google_client_id: str = ...
    google_client_secret: str = ...
    google_token_url: str = ...
    google_base_url: str = ...
    google_userinfo_url: str = ...
    google_redirect_url: str = ...
    model_config: str = SettingsConfigDict(env_prefix='auth_')


class RedisSettings(BaseSettings):
    host: str = ...
    port: int = ...

    model_config = SettingsConfigDict(env_prefix='redis_')


class RabbitSettings(BaseSettings):
    host: str = ...
    port: int = ...
    user: str = ...
    password: str = ...

    model_config = SettingsConfigDict(env_prefix='rabbit_')


class CronSettings(BaseSettings):
    sec: int = 10



class APPSettings(BaseSettings):
    project_name: str = 'Notifications API'
    redis: RedisSettings = RedisSettings()
    rabbit: RabbitSettings = RabbitSettings()
    auth: AuthSettings = AuthSettings()
    mongo: MongoSettings = MongoSettings()
    rabbit_dsn: str = f"amqp://{rabbit.user}:{rabbit.password}@{rabbit.host}:{rabbit.port}"


settings = APPSettings()
