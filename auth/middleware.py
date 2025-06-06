from fastapi import Request, HTTPException
import os

VALID_TOKEN = os.getenv("API_AUTH_TOKEN")

async def verify_token(request: Request, call_next):
    if request.url.path.startswith("/dashboard") or request.url.path.startswith("/bot"):
        token = request.headers.get("Authorization")
        if not token or token.replace("Bearer ", "") != VALID_TOKEN:
            raise HTTPException(status_code=401, detail="Unauthorized")
    response = await call_next(request)
    return response
