import json
from app.services.company_api import get_company_api

api = get_company_api()

SUPPORT_TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_order",
            "description": "Get information about a customer's order by order ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID, e.g., '1001'"
                    }
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer",
            "description": "Get information about a customer by customer ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The customer ID, e.g., 'customer-001'"
                    }
                },
                "required": ["customer_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_ticket",
            "description": "Create a new support ticket for a customer issue.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The customer ID. Pass 'unknown' if not known."
                    },
                    "issue": {
                        "type": "string",
                        "description": "Description of the customer's issue."
                    }
                },
                "required": ["customer_id", "issue"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_ticket",
            "description": "Update the status of an existing support ticket.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "The ticket ID, e.g., 'TKT-001'"
                    },
                    "status": {
                        "type": "string",
                        "description": "The new status of the ticket."
                    }
                },
                "required": ["ticket_id", "status"]
            }
        }
    }
]

async def execute_tool(name: str, arguments: dict) -> str:
    """Executes a tool by name and returns a JSON string result."""
    try:
        if name == "get_order":
            result = await api.get_order(arguments.get("order_id"))
            return json.dumps(result) if result else json.dumps({"error": "Order not found."})
        elif name == "get_customer":
            result = await api.get_customer(arguments.get("customer_id"))
            return json.dumps(result) if result else json.dumps({"error": "Customer not found."})
        elif name == "create_ticket":
            result = await api.create_ticket(arguments.get("customer_id"), arguments.get("issue"))
            return json.dumps(result)
        elif name == "update_ticket":
            result = await api.update_ticket(arguments.get("ticket_id"), arguments.get("status"))
            return json.dumps(result) if result else json.dumps({"error": "Ticket not found."})
        else:
            return json.dumps({"error": f"Unknown tool: {name}"})
    except Exception as e:
        return json.dumps({"error": str(e)})
