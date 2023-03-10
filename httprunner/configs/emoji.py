from pydantic import BaseSettings


class Emojis(BaseSettings):
    success: str = "✔️"
    failure: str = "❌"


emojis = Emojis()
