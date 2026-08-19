import json
from openai import AsyncOpenAI
from app.config import settings
from app.models.schemas import IncomingMessage, AgentResponse
from app.agents import support_agent, sales_agent, hr_agent

ROUTER_PROMPT = """
You are a Supervisor Agent. 
Your job is to read the user's message and decide which specialized agent should handle it.

The available agents are:
- support: Handles general customer support, order checking, and complaints.
- hr: Handles employee leave balances, expenses, and HR policies.
- sales: Handles product pricing, inventory checks, and sales inquiries.

You must respond with ONLY a JSON object in the following format:
{"agent": "support"}
{"agent": "hr"}
{"agent": "sales"}

Do not include any other text, just the JSON.
"""

client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL
)

async def handle_message(incoming: IncomingMessage) -> AgentResponse:
    try:
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": ROUTER_PROMPT},
                {"role": "user", "content": incoming.message}
            ],
            response_format={"type": "json_object"}
        )
        
        result_text = response.choices[0].message.content
        result_json = json.loads(result_text)
        selected_agent = result_json.get("agent", "support")
        
        # Route to the appropriate agent
        if selected_agent == "hr":
            sub_response = await hr_agent.handle_message(incoming)
        elif selected_agent == "sales":
            sub_response = await sales_agent.handle_message(incoming)
        else:
            sub_response = await support_agent.handle_message(incoming)
            
        # Append the routing info to metadata so the UI can visualize it
        sub_response.metadata["routed_by"] = "orchestrator"
        sub_response.metadata["original_selection"] = selected_agent
        
        return sub_response
        
    except Exception as e:
        return AgentResponse(
            success=False,
            conversation_id=incoming.conversation_id,
            agent="orchestrator",
            text=f"Orchestrator failed to route: {str(e)}",
            metadata={"error": str(e)}
        )
