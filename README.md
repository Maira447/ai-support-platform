# AI Customer Support Platform

A complete, modular, production-ready AI customer-support platform using the OpenAI Agents SDK and FastAPI. This platform is capable of receiving natural-language customer messages and responding intelligently in English, Urdu, and Roman Urdu.

## Architecture

The system is designed in three decoupled phases to keep the core AI logic completely independent of channel implementations.

### Local Development Flow
```text
Local Test Client
       ↓
 Agent Gateway
       ↓
 OpenAI Agents SDK (Support Agent)
       ↓
     Tools
       ↓
  Mock API
```

### Veevo WhatsApp Flow
```text
  WhatsApp
       ↓
    Webhook
       ↓
 Agent Gateway
       ↓
 OpenAI Agents SDK (Support Agent)
       ↓
     Tools
       ↓
 Real Veevo API
```

### VT Platform Flow (Future Integration)
```text
 VT AI Platform Worker
       ↓
    VT Adapter
       ↓
 Agent Gateway
       ↓
 OpenAI Agents SDK (Support Agent)
```

## Setup

1. **Clone and navigate to the project directory:**
   ```bash
   cd ai-support-platform
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required).
- `OPENAI_MODEL`: The LLM model to use (default: `gpt-4o`).
- `ENVIRONMENT`: deployment environment (`development`, `production`).
- `MOCK_MODE`: Set to `true` to use mock data for orders and tickets. Set to `false` when connecting to a real API.
- `AGENT_API_KEY`: Secret key used for authenticating local gateway testing.
- `VEEVO_API_BASE_URL`: Base URL for Veevo API (required for Phase 2).
- `VEEVO_API_KEY`: Your Veevo API key (required for Phase 2).
- `VEEVO_WHATSAPP_WEBHOOK_SECRET`: Webhook verification secret (required for Phase 2).
- `VEEVO_WHATSAPP_PHONE_ID`: Sender phone ID for WhatsApp (required for Phase 2).

## Local Testing

### 1. Run the Server
Start the FastAPI server:
```bash
python run.py
```
Check the API documentation at: http://localhost:8000/docs

### 2. Run Automated Test Scenarios
Run the automated test client (tests English, Urdu, Roman Urdu, and ticket creation):
```bash
python test_client.py
```

### 3. Run Interactive CLI Chat
Have a real-time terminal conversation with the Support Agent:
```bash
python chat.py
```

## Mock Mode
When `MOCK_MODE=true`, the system uses `mock_data/orders.json`, `mock_data/customers.json`, and `mock_data/tickets.json` instead of a real API. 

## WhatsApp Integration
The `app/adapters/whatsapp_adapter.py` handles Veevo WhatsApp webhooks. 
- You can test a mock WhatsApp payload locally by POSTing to `/api/test/whatsapp`.
- **Note:** Real Veevo WhatsApp is NOT connected. Real credentials, a configured Webhook URL (e.g. via ngrok), and the actual Veevo Webhook JSON documentation are required before the production webhook `/webhooks/veevo/whatsapp` can be finalized.

## VT Integration Placeholder
The `app/adapters/vt_adapter.py` provides an isolated `VTAdapter` placeholder.
- **Status:** Not implemented.
- **Required Information:** Before this can be implemented, actual documentation for the VT Platform/Worker webhook payload structure, authentication method, and API response format is required. Do not assume fields or endpoints.

## Docker
You can run the entire platform via Docker:
```bash
docker compose up --build
```

## Testing Suite
Run the test suite via pytest:
```bash
pytest
```
