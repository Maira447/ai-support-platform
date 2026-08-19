import asyncio
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

async def main():
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.groq.com/openai/v1")
    model = os.getenv("OPENAI_MODEL", "llama-3.1-70b-versatile")
    
    print(f"Testing key: {api_key[:8]}...{api_key[-4:] if api_key else ''}")
    print(f"Base URL: {base_url}")
    print(f"Model: {model}")
    
    client = AsyncOpenAI(api_key=api_key, base_url=base_url)
    
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hello!"}]
        )
        print("Success! Response:")
        print(response.choices[0].message.content)
    except Exception as e:
        print("Error:")
        print(e)

if __name__ == "__main__":
    asyncio.run(main())
