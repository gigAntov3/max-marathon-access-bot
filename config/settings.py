from typing import List, Dict

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class BotConfig(BaseModel):
    token: str = "f9LHodD0cOI__Q3Znx9Pb9_F7phO9AO36e6jugl_Lq4XlYJob4caGGKalOW3i0ck13ejp0Tx6g6lF9jNP4ml"

    admin_password: str = "1111"

    admins: List[int] = [96966830]


class DatabaseConfig(BaseModel):
    url: str = "sqlite+aiosqlite:///data/database.db"
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class PaymentConfig(BaseModel):
    shop_id: str = "1038936"
    secret_key: str = "test_m56xrOAANO_0p6qQIDv35_t8MQMj5ldn0uJowtYExu8"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    bot: BotConfig = BotConfig()
    database: DatabaseConfig = DatabaseConfig()
    payment: PaymentConfig = PaymentConfig()


settings = Settings()