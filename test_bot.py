import os
from dotenv import load_dotenv
import httpx
import asyncio

# 1. This command looks for the .env file and loads it into memory
load_dotenv()

# 2. Now we grab the variables using os.getenv
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


async def test_connection():
    # 3. Always add a safety check for a better developer experience
    if not TOKEN or not CHAT_ID:
        print("ERROR: Secrets not found!")
        return

    print(f"Found Token: {TOKEN[:5]}.")

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": "Local .env test successful! Telegram is connected."
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        if response.status_code == 200:
            print("Success! Check your Telegram.")
        else:
            print(f"⚠Failed: {response.text}")


if __name__ == "__main__":
    asyncio.run(test_connection())