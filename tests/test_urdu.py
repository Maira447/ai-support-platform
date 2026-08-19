import pytest
from app.adapters.local_adapter import handle_local_message, LocalMessageRequest

@pytest.mark.asyncio
async def test_urdu_and_english():
    # Test English
    req_en = LocalMessageRequest(
        user_id="test-en",
        conversation_id="conv-en",
        message="Where is my order 1001?"
    )
    res_en = await handle_local_message(req_en)
    assert res_en.success is True
    assert "tools_used" in res_en.metadata
    
    # Test Urdu
    req_ur = LocalMessageRequest(
        user_id="test-ur",
        conversation_id="conv-ur",
        message="mera order 1001 kahan hai?"
    )
    res_ur = await handle_local_message(req_ur)
    assert res_ur.success is True
    assert "tools_used" in res_ur.metadata
