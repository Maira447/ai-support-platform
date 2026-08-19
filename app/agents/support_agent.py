import json
from openai import AsyncOpenAI
from app.config import settings
from app.models.schemas import IncomingMessage, AgentResponse
from app.services.session_service import session_manager
from app.tools.support_tools import SUPPORT_TOOLS_SCHEMA, execute_tool

SYSTEM_PROMPT = """
You are the company's Customer Support Agent.

Your responsibilities:
- Help customers with orders.
- Help customers with support issues.
- Check order information using tools.
- Create support tickets when necessary.
- Never invent company information.
- Never invent order status.
- Never claim that an action happened unless the corresponding tool confirms it.

Languages:
- English
- Urdu
- Roman Urdu

Respond naturally in the customer's language.
If the customer writes in Urdu, respond in Urdu.
If the customer writes in Roman Urdu, respond in Roman Urdu.
If the customer writes in English, respond in English.
If an order number is missing, ask the customer for it.
Keep responses concise and customer-friendly.
"""

client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL
)

async def handle_message(incoming: IncomingMessage) -> AgentResponse:
    # 1. Fetch history
    history = session_manager.get_history(incoming.channel, incoming.user_id, incoming.conversation_id)
    if not history:
        history.append({"role": "system", "content": SYSTEM_PROMPT})
    
    # 2. Append new user message
    user_msg = {"role": "user", "content": incoming.message}
    history.append(user_msg)
    session_manager.append_message(incoming.channel, incoming.user_id, incoming.conversation_id, user_msg)

    tools_used = []

    # 3. Agent Loop (handle tool calls)
    while True:
        try:
            response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=history,
                tools=SUPPORT_TOOLS_SCHEMA,
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            
            # Append assistant message to history
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
                # Continue loop to send tool results back to model
                continue
            else:
                # Final response generated
                return AgentResponse(
                    success=True,
                    conversation_id=incoming.conversation_id,
                    agent="support",
                    text=message.content or "",
                    metadata={"tools_used": tools_used}
                )
                
        except Exception as e:
            return AgentResponse(
                success=False,
                conversation_id=incoming.conversation_id,
                agent="support",
                text=f"An error occurred: {str(e)}",
                metadata={"error": str(e)}
            )
