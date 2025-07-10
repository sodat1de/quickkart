import os
import httpx

USER_SVC_URL = os.getenv("USER_SERVICE_URL", "http://user-svc:8000")


async def validate_jwt(token: str):
    """Calls the user-svc /verify endpoint; raises HTTPStatusError if invalid."""
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{USER_SVC_URL}/verify", headers=headers, timeout=5.0)
        r.raise_for_status()
        return r.json()  # user object
