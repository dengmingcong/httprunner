from pydantic import BaseSettings


class Emojis(BaseSettings):
    success: str = "✔️"
    fail: str = "❌"


emojis = Emojis()
