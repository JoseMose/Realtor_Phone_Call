from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    openai_api_key: str
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str = "+1234567890"
    webhook_base_url: str = os.getenv("WEBHOOK_BASE_URL", "https://nonlactic-unvenerative-elisha.ngrok-free.dev")

    class Config:
        env_file = ".env"

settings = Settings()