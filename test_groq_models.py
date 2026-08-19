import asyncio
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

async def main():
    load_dotenv(override=True)
    
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.groq.com/openai/v1")
    
    client = AsyncOpenAI(api_key=api_key, base_url=base_url)
    
    try:
        models = await client.models.list()
        for m in models.data:
            print(m.id)
    except Exception as e:
        print("Error:")
        print(e)

if __name__ == "__main__":
    asyncio.run(main())
