from pydantic import BaseModel
from typing import Dict, Any
from app.models.schemas import IncomingMessage
from app.agents.registry import get_agent_handler
import logging

logger = logging.getLogger(__name__)

class TestWhatsAppRequest(BaseModel):
    from_number: str
    message: str

async def simulate_whatsapp_message(request: TestWhatsAppRequest) -> Dict[str, Any]:
    """Simulates receiving a WhatsApp message locally."""
    incoming = IncomingMessage(
        channel="whatsapp",
        user_id=request.from_number,
        conversation_id=f"wa-{request.from_number}",
        message=request.message,
        metadata={"simulated": True}
    )
    
    handler = get_agent_handler("support")
    response = await handler(incoming)
    
    return {
        "status": "success",
        "simulated_outbound": {
            "to": request.from_number,
            "text": response.text
        }
    }

async def handle_veevo_webhook(payload: Dict[Any, Any]) -> Dict[str, Any]:
    """
    Actual Veevo WhatsApp Webhook Parser.
    TODO: Parse the actual Veevo webhook JSON structure here once documented.
    """
    logger.info("Received Veevo webhook payload")
    
    # Fake parsing for now to demonstrate flow
    # In reality, verify signature, extract from_number, message text, message ID, etc.
    
    return {"status": "received"}

class VeevoWhatsAppClient:
    """Outbound client for Veevo WhatsApp API."""
    def __init__(self, api_url: str, api_key: str, phone_id: str):
        self.api_url = api_url
        self.api_key = api_key
        self.phone_id = phone_id

    async def send_text_message(self, to: str, text: str):
        """
        TODO: Implement real HTTP request to Veevo API to send a message.
        """
        logger.info(f"Sending WhatsApp to {to}: {text}")
        pass
