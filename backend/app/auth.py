import time
from typing import Any, Dict, Optional

import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from .config import settings

security = HTTPBearer()

# ---------- JWKS キャッシュ（1時間） ----------
_jwks_cache: Optional[Dict[str, Any]] = None
_jwks_fetched_at: float = 0
_JWKS_TTL = 3600


def _fetch_jwks() -> Dict[str, Any]:
    """Supabase JWKS エンドポイントから公開鍵セットを取得する。結果を1時間キャッシュ。"""
    global _jwks_cache, _jwks_fetched_at

    if _jwks_cache and time.time() - _jwks_fetched_at < _JWKS_TTL:
        return _jwks_cache

    url = f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json"
    try:
        res = httpx.get(url, timeout=10)
        res.raise_for_status()
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to fetch JWKS: {e}",
        )

    _jwks_cache = res.json()
    _jwks_fetched_at = time.time()
    return _jwks_cache


def _get_public_key(kid: str) -> Dict[str, Any]:
    """kid に一致する JWK を返す。見つからない場合は JWKS を再取得して再試行。"""
    for refresh in (False, True):
        if refresh:
            global _jwks_cache
            _jwks_cache = None  # キャッシュ強制クリア（鍵ローテーション対応）
        jwks = _fetch_jwks()
        key = next((k for k in jwks.get("keys", []) if k.get("kid") == kid), None)
        if key:
            return key

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Public key not found for kid: {kid}",
    )


# ---------- FastAPI Dependency ----------

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """
    Supabase JWT（ES256）を検証して user_id（sub）を返す。

    検証フロー:
      1. JWT ヘッダーから kid を取得
      2. JWKS から対応する EC 公開鍵を取得（キャッシュ付き）
      3. ES256 で署名検証
      4. sub クレームを返す
    """
    token = credentials.credentials
    try:
        header = jwt.get_unverified_header(token)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token header: {e}",
        )

    kid = header.get("kid")
    if not kid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing kid",
        )

    public_key = _get_public_key(kid)

    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["ES256"],
            options={"verify_aud": False},
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {e}",
        )

    user_id: Optional[str] = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing sub",
        )

    return user_id
