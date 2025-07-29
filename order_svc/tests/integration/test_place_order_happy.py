import httpx, os, pytest, jwt

base = "http://localhost"

@pytest.mark.integration
@pytest.mark.asyncio
async def test_order_flow_running_compose():
    # 1. health
    async with httpx.AsyncClient() as c:
        for port in (8000, 8001, 8002, 8010):
            r = await c.get(f"{base}:{port}/healthz", timeout=3)
            assert r.status_code == 200

        # 2. bootstrap product
        p = {"name": "USB‑C cable", "price": 9.99}
        await c.post(f"{base}:8001/products", json=p)

        # 3. register + login
        creds = {"email": "bob@example.com", "password": "secret"}
        await c.post(f"{base}:8000/register", json=creds)
        tok = (
            await c.post(f"{base}:8000/login", json=creds)
        ).json()["access_token"]

        # 4. place order
        hdrs = {"Authorization": f"Bearer {tok}"}
        r = await c.post(f"{base}:8002/orders", json={"item": p["name"]}, headers=hdrs)
        assert r.status_code == 201
