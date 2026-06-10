from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    rebrickable_api_key: str = ""
    bricklink_consumer_key: str = ""
    bricklink_consumer_secret: str = ""
    bricklink_token_value: str = ""
    bricklink_token_secret: str = ""
    host: str = "0.0.0.0"
    port: int = 8000

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
