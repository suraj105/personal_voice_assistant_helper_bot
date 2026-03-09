import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, BackgroundTasks
import httpx

# 1. Load secrets
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 2. Initialize FastAPI
app = FastAPI()


# 3. Helper function with Debugging
async def send_telegram_msg(summary: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": f"🍕 *NEUE BESTELLUNG*\n\n{summary}",
        "parse_mode": "Markdown"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload)
            # This will show us if Telegram accepted the message
            if response.status_code == 200:
                print("✅ SUCCESS: Telegram message sent!")
            else:
                print(f"TELEGRAM ERROR {response.status_code}: {response.text}")
        except Exception as e:
            print(f"CONNECTION ERROR: {e}")


# 4. The "Webhook" endpoint that Vapi will call
@app.post("/webhook")
async def handle_vapi_call(request: Request, background_tasks: BackgroundTasks):
    # Get the JSON data from Vapi
    data = await request.json()

    # We only care about the 'end-of-call-report'
    message_type = data.get("message", {}).get("type")

    if message_type == "end-of-call-report":
        # Extract the summary created by Gemini 3 Flash
        summary = data.get("message", {}).get("analysis", {}).get("summary", "No summary.")

        # Send to Telegram in the background (so Vapi gets a fast 200 OK response)
        background_tasks.add_task(send_telegram_msg, summary)

    return {"status": "success"}


# 5. Root endpoint for testing
@app.get("/")
def read_root():
    return {"message": "API call is working"}