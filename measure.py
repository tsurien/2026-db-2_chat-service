import hashlib
import json
import sys
import time
import urllib.request

from app.redis_client import r

sys.stdout.reconfigure(encoding="utf-8")

BASE = "http://127.0.0.1:8000"
# TOKEN = "여기에_access_token_붙여넣기"
TOKEN = "eyJhbGciOiJFUzI1NiIsImtpZCI6IjBiMjc5ZmYyLTI0MGYtNGE4Zi1iNmE5LTdlNzJlM2FjZTExOCIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2h3cm9hYWh3YnJsbHVmZm1kZWx1LnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiIwYzczMzM0ZS0zMmUzLTQ4YTktOTc0Ny0wNTQwNjBjN2U4MDUiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzg3ODE1NTYzLCJpYXQiOjE3ODc4MTE5NjMsImVtYWlsIjoicmxzLWFAZXhhbXBsZS5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIiwicHJvdmlkZXJzIjpbImVtYWlsIl19LCJ1c2VyX21ldGFkYXRhIjp7ImVtYWlsIjoicmxzLWFAZXhhbXBsZS5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGhvbmVfdmVyaWZpZWQiOmZhbHNlLCJzdWIiOiIwYzczMzM0ZS0zMmUzLTQ4YTktOTc0Ny0wNTQwNjBjN2U4MDUifSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJwYXNzd29yZCIsInRpbWVzdGFtcCI6MTc4NzgxMTk2M31dLCJzZXNzaW9uX2lkIjoiZWExMTc5Y2YtODUyMy00NjNhLWJhMTMtYTM3MzhjMzU2N2ZlIiwiaXNfYW5vbnltb3VzIjpmYWxzZX0.OGEp3yQuys1JfBZHXl-YPeeQ1x5-AQ8ACxxwcxOFbxBA-H_Y129KXvyvWCJ9TuRD79m9O9I4XicUJZZGyXp9Ag"
CONVERSATION_ID = "0881f97c-ef58-4fc7-9b9d-e13edbfa91c5"


def call(path):
    req = urllib.request.Request(BASE + path)
    req.add_header("Authorization", "Bearer " + TOKEN)
    started = time.perf_counter()
    with urllib.request.urlopen(req) as res:
        body = json.loads(res.read())
    return body, (time.perf_counter() - started) * 1000


def measure(path, cache_key, times=3):
    """캐시를 비우고 같은 요청을 여러 번 보낸다."""
    r.delete(cache_key)          # 1회차가 확실히 MISS 가 되게 한다
    print(f"\n{path}")
    for i in range(1, times + 1):
        body, ms = call(path)
        count = len(body) if isinstance(body, list) else "-"
        print(f"  {i}회차  {ms:7.1f} ms  {count}건  남은 TTL {r.ttl(cache_key):>4}s")


measure("/me", "session:" + hashlib.sha256(TOKEN.encode()).hexdigest())
measure(f"/conversations/{CONVERSATION_ID}/messages", f"messages:{CONVERSATION_ID}")