from pydantic_settings import BaseSettings, SettingsConfigDict


class Emojis(BaseSettings):
    success: str = "✔️"
    failure: str = "❌"
    model_config = SettingsConfigDict(env_prefix="httprunner_emoji_")


emojis = Emojis()
