from fastapi import APIRouter, Depends
from typing import Dict, Any
from app.api.auth import verify_api_key
from app.adapters.local_adapter import LocalMessageRequest, handle_local_message
from app.adapters.whatsapp_adapter import (
    simulate_whatsapp_message, 
    handle_veevo_webhook,
    TestWhatsAppRequest
)
from app.adapters.vt_adapter import handle_vt_message

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.post("/api/local/message")
async def local_message_endpoint(
    request: LocalMessageRequest, 
    api_key: str = Depends(verify_api_key)
):
    """Local development and testing endpoint."""
    response = await handle_local_message(request)
    return {
        "success": response.success,
        "agent": response.agent,
        "conversation_id": response.conversation_id,
        "response": response.text,
        "metadata": response.metadata
    }

@router.post("/api/test/whatsapp")
async def test_whatsapp_endpoint(
    request: TestWhatsAppRequest,
    api_key: str = Depends(verify_api_key)
):
    """Simulates an incoming WhatsApp message without needing Veevo."""
    return await simulate_whatsapp_message(request)

@router.post("/webhooks/veevo/whatsapp")
async def veevo_whatsapp_webhook(payload: Dict[Any, Any]):
    """Actual webhook endpoint for Veevo WhatsApp integration."""
    return await handle_veevo_webhook(payload)

@router.post("/api/vt/message")
async def vt_message_endpoint(payload: Dict[Any, Any]):
    """Placeholder endpoint for VT integration."""
    return await handle_vt_message(payload)
