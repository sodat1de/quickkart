import os, httpx

USER_SVC_URL   = os.getenv("USER_SERVICE_URL", "http://user-svc:8000")
PRODUCT_SVC_URL= os.getenv("PRODUCT_SERVICE_URL", "http://product-svc:8000")
NOTIFY_SVC_URL = os.getenv("NOTIFY_SERVICE_URL", "http://notify-svc:8010")

async def validate_jwt(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{USER_SVC_URL}/verify", headers=headers, timeout=5)
        r.raise_for_status()
        return r.json()

def product_exists(item: str):
    r = httpx.get(f"{PRODUCT_SVC_URL}/products")
    r.raise_for_status()
    return any(p["name"] == item for p in r.json())

async def email_confirmation(user_email: str, item: str):
    async with httpx.AsyncClient() as c:
        await c.post(f"{NOTIFY_SVC_URL}/email", params={"user_email": user_email, "item": item})