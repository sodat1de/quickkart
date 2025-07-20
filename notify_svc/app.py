from fastapi import FastAPI, BackgroundTasks
from prometheus_fastapi_instrumentator import Instrumentator
import emailer

app = FastAPI(title="QuickKart Notification Service")
Instrumentator().instrument(app).expose(app)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/email")
async def send_email(user_email: str, item: str, bg: BackgroundTasks):
    # called by order-svc
    bg.add_task(emailer.send_confirmation, user_email, item)
    return {"sent": True}