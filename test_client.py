import httpx
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("AGENT_API_KEY", "local-dev-key")
HEADERS = {"X-Agent-Api-Key": API_KEY}
BASE_URL = "http://localhost:8000"

async def test_message(msg: str):
    print(f"\nUser: {msg}")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/api/local/message",
            json={
                "user_id": "tester-001",
                "conversation_id": "test-conv-001",
                "message": msg
            },
            headers=HEADERS,
            timeout=30.0
        )
        if response.status_code == 200:
            data = response.json()
            print(f"Agent: {data['response']}")
            print(f"Agent used: {data['agent']}")
            print(f"Tools used: {data['metadata'].get('tools_used', [])}")
        else:
            print(f"Error: {response.text}")

async def main():
    print("==================================")
    print("AI Customer Support - Test Client")
    print("==================================")
    
    messages = [
        "Where is my order 1001?",
        "میرا آرڈر 1001 کہاں ہے؟",
        "mera order 1001 kahan hai?",
        "mera payment fail ho gaya hai ticket bana dein",
        "Can you check order 9999?",
        "Thanks, when will 1001 arrive?"
    ]
    
    for msg in messages:
        await test_message(msg)
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
