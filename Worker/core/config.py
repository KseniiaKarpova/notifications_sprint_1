from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


load_dotenv()


class AdminSettings(BaseSettings):
    login: str = ...
    password: str = ...
    email: str = ...

    model_config: str = SettingsConfigDict(env_prefix='admin_')


class WebsocketSettings(BaseSettings):
    host: str = ...
    port: str = ...
    model_config: str = SettingsConfigDict(env_prefix='websocket_')

    @property
    def send_message_url(self):
        return f"http://{self.host}:{self.port}/api/v1/send"


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
    api_host: str = ...
    api_port: int = ...
    jwt_algorithm: str = ...
    google_client_id: str = ...
    google_client_secret: str = ...
    google_token_url: str = ...
    google_base_url: str = ...
    google_userinfo_url: str = ...
    google_redirect_url: str = ...
    model_config: str = SettingsConfigDict(env_prefix='auth_')

    @property
    def api_url(self):
        return f"http://{self.api_host}:{self.api_port}/api/v1"


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
    @property
    def dsn(self):
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}"


class CronSettings(BaseSettings):
    sec: int = 10



class APPSettings(BaseSettings):
    project_name: str = 'Notifications API'
    redis: RedisSettings = RedisSettings()
    rabbit: RabbitSettings = RabbitSettings()
    auth: AuthSettings = AuthSettings()
    mongo: MongoSettings = MongoSettings()
    admin: AdminSettings = AdminSettings()
    websocket: WebsocketSettings = WebsocketSettings()


settings = APPSettings()
