from pydantic import BaseModel
from typing import Optional
from app.models.schemas import IncomingMessage, AgentResponse
from app.agents.registry import get_agent_handler

class LocalMessageRequest(BaseModel):
    user_id: Optional[str] = "local-tester"
    conversation_id: str = "conv-001"
    message: str
    agent: Optional[str] = "orchestrator"

async def handle_local_message(request: LocalMessageRequest) -> AgentResponse:
    # Convert to normalized internal format
    incoming = IncomingMessage(
        channel="local",
        user_id=request.user_id,
        conversation_id=request.conversation_id,
        message=request.message,
        metadata={}
    )
    
    # Route to appropriate agent
    handler = get_agent_handler(request.agent or "orchestrator")
    response = await handler(incoming)
    
    return response
