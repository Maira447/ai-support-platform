import json

HR_TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_leave_balance",
            "description": "Get the leave balance for an employee.",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "string",
                        "description": "The ID of the employee (e.g., EMP123)."
                    }
                },
                "required": ["employee_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "submit_expense",
            "description": "Submit an expense report for an employee.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "number",
                        "description": "The expense amount."
                    },
                    "category": {
                        "type": "string",
                        "description": "The category of the expense (e.g., Travel, Meals)."
                    }
                },
                "required": ["amount", "category"]
            }
        }
    }
]

async def execute_tool(name: str, args: dict) -> str:
    """Mock execution of HR tools."""
    if name == "get_leave_balance":
        # Mock logic
        emp_id = args.get("employee_id")
        return json.dumps({
            "employee_id": emp_id,
            "annual_leave": 14,
            "sick_leave": 5,
            "status": "success"
        })
    elif name == "submit_expense":
        # Mock logic
        amount = args.get("amount")
        category = args.get("category")
        return json.dumps({
            "status": "success",
            "message": f"Expense of {amount} for {category} submitted successfully. Pending approval.",
            "reference_id": "EXP-98765"
        })
    return json.dumps({"error": f"Tool {name} not found"})
