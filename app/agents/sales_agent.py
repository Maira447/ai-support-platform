import json
from openai import AsyncOpenAI
from app.config import settings
from app.models.schemas import IncomingMessage, AgentResponse
from app.services.session_service import session_manager
from app.tools.sales_tools import SALES_TOOLS_SCHEMA, execute_tool

SYSTEM_PROMPT = """
You are the company's Sales Representative.

Your responsibilities:
- Answer questions about product prices and inventory.
- Persuade customers to buy our products.
- Use tools to check stock and pricing.
- Be enthusiastic and polite.
"""

client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL
)

async def handle_message(incoming: IncomingMessage) -> AgentResponse:
    history = session_manager.get_history(incoming.channel, incoming.user_id, incoming.conversation_id)
    if not history:
        history.append({"role": "system", "content": SYSTEM_PROMPT})
    
    user_msg = {"role": "user", "content": incoming.message}
    history.append(user_msg)
    session_manager.append_message(incoming.channel, incoming.user_id, incoming.conversation_id, user_msg)

    tools_used = []

    while True:
        try:
            response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=history,
                tools=SALES_TOOLS_SCHEMA,
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            history.append(message.model_dump(exclude_none=True))
            session_manager.append_message(incoming.channel, incoming.user_id, incoming.conversation_id, message.model_dump(exclude_none=True))
            
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    tools_used.append(tool_call.function.name)
                    args = json.loads(tool_call.function.arguments)
                    tool_result = await execute_tool(tool_call.function.name, args)
                    
                    tool_msg = {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": tool_result
                    }
                    history.append(tool_msg)
                    session_manager.append_message(incoming.channel, incoming.user_id, incoming.conversation_id, tool_msg)
                continue
            else:
                return AgentResponse(
                    success=True,
                    conversation_id=incoming.conversation_id,
                    agent="sales",
                    text=message.content or "",
                    metadata={"tools_used": tools_used}
                )
                
        except Exception as e:
            return AgentResponse(
                success=False,
                conversation_id=incoming.conversation_id,
                agent="sales",
                text=f"An error occurred: {str(e)}",
                metadata={"error": str(e)}
            )
