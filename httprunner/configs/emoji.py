from pydantic import BaseSettings


class Emojis(BaseSettings):
    success: str = "✔️"
    failure: str = "❌"

    class Config:
        env_prefix = "httprunner_emoji_"


emojis = Emojis()
