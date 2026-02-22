from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_SERVICE_KEY: str
    OPENAI_API_KEY: str = ""
    STORAGE_BUCKET: str = "audio"

    model_config = {"env_file": ".env"}


settings = Settings()
