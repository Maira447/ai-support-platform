import json

SALES_TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_product_price",
            "description": "Get the current price and details of a product.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "The name of the product."
                    }
                },
                "required": ["product_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_inventory",
            "description": "Check if a product is in stock.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "The name of the product."
                    }
                },
                "required": ["product_name"]
            }
        }
    }
]

async def execute_tool(name: str, args: dict) -> str:
    """Mock execution of Sales tools."""
    if name == "get_product_price":
        # Mock logic
        product = args.get("product_name")
        return json.dumps({
            "product_name": product,
            "price": "$99.99",
            "currency": "USD",
            "discount_available": True
        })
    elif name == "check_inventory":
        # Mock logic
        product = args.get("product_name")
        return json.dumps({
            "product_name": product,
            "in_stock": True,
            "stock_count": 150,
            "warehouse_location": "US-East"
        })
    return json.dumps({"error": f"Tool {name} not found"})
