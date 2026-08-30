

from dataclasses import dataclass

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.db import get_anon_client
# from app.redis_client import r
from app.cache import cache_get, cache_set

import hashlib
import json

bearer_scheme = HTTPBearer()

SESSION_CACHE_TTL_SECONDS = 300

@dataclass
class CurrentUser:
    id: str
    email: str
    token: str

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> CurrentUser:
    token = credentials.credentials
    cache_key = f"session:{hashlib.sha256(token.encode()).hexdigest()}"

    cached = r.get(cache_key)
    if cached:
        data = json.loads(cached)
        return CurrentUser(id=data["id"], email=data["email"], token=token)

    client = get_anon_client()
    try:
        result = client.auth.get_user(token)
    except Exception:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")

    current_user = CurrentUser(
                        id=str(result.user.id),
                        email=result.user.email,
                        token=token)

    # cached = cache_get(cache_key)
    
    cache_set(cache_key,
        json.dumps({"id": current_user.id,
                    "email": current_user.email
                    }),
        SESSION_CACHE_TTL_SECONDS,
    )
    # r.set(
    #     cache_key,
    #     json.dumps({"id": current_user.id,
    #                 "email": current_user.email}),
    #     ex=SESSION_CACHE_TTL_SECONDS,
    # )
    return current_user