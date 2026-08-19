from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class IncomingMessage(BaseModel):
    channel: str
    user_id: Optional[str] = None
    conversation_id: str
    message: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AgentResponse(BaseModel):
    success: bool
    conversation_id: str
    agent: str
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
