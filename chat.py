import httpx
import asyncio
from dotenv import load_dotenv
import os
import uuid

load_dotenv()
API_KEY = os.getenv("AGENT_API_KEY", "local-dev-key")
HEADERS = {"X-Agent-Api-Key": API_KEY}
BASE_URL = "http://localhost:8000"

async def chat():
    print("==================================")
    print("AI Customer Support Demo")
    print("==================================")
    print("Type 'exit' to quit.\n")
    
    conv_id = str(uuid.uuid4())
    
    async with httpx.AsyncClient() as client:
        while True:
            try:
                user_msg = input("You: ")
                if user_msg.lower() in ['exit', 'quit']:
                    break
                
                response = await client.post(
                    f"{BASE_URL}/api/local/message",
                    json={
                        "user_id": "chat-user",
                        "conversation_id": conv_id,
                        "message": user_msg
                    },
                    headers=HEADERS,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"\nAgent: {data['response']}\n")
                else:
                    print(f"\nError: {response.text}\n")
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"\nError: {e}\n")

if __name__ == "__main__":
    asyncio.run(chat())
