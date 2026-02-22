from typing import Optional

from supabase import Client, create_client

from .config import settings

_client: Optional[Client] = None


def get_supabase() -> Client:
    """サービスロールキーで初期化したSupabaseクライアント（シングルトン）"""
    global _client
    if _client is None:
        _client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
    return _client
