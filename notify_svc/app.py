from fastapi import FastAPI, BackgroundTasks
import emailer

app = FastAPI(title="QuickKart Notification Service")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/email")
async def send_email(user_email: str, item: str, bg: BackgroundTasks):
    # called by order-svc
    bg.add_task(emailer.send_confirmation, user_email, item)
    return {"sent": True}