import os, aiosmtplib, email.message

SMTP_HOST = os.getenv("SMTP_HOST", "mailhog")
SMTP_PORT = int(os.getenv("SMTP_PORT", "1025"))
FROM_ADDR = os.getenv("FROM_ADDR", "no-reply@quickkart.local")

async def send_confirmation(to_addr: str, item: str):
    msg = email.message.EmailMessage()
    msg["From"] = FROM_ADDR
    msg["To"] = to_addr
    msg["Subject"] = "Your QuickKart order"
    msg.set_content(f"Thank you for ordering \"{item}\". We will ship soon!")

    await aiosmtplib.send(msg, hostname=SMTP_HOST, port=SMTP_PORT)