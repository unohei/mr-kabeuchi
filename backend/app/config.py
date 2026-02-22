from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_SERVICE_KEY: str
    OPENAI_API_KEY: str = ""
    STORAGE_BUCKET: str = "audio"
    # カンマ区切りで複数指定可（本番URLを追加する）
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:4173"

    model_config = {"env_file": ".env"}


settings = Settings()
