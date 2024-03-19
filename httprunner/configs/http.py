from pydantic_settings import BaseSettings, SettingsConfigDict


class GlobalHttpSettings(BaseSettings):
    headers: dict = {}
    model_config = SettingsConfigDict(env_prefix="global_http_")


global_http_settings = GlobalHttpSettings()
