import json
import os
from typing import Dict, Any, Optional
from app.config import settings

class CompanyAPIInterface:
    async def get_customer(self, customer_id: str) -> Optional[Dict[str, Any]]:
        pass

    async def get_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        pass

    async def create_ticket(self, customer_id: str, issue: str) -> Dict[str, Any]:
        pass

    async def update_ticket(self, ticket_id: str, status: str) -> Optional[Dict[str, Any]]:
        pass

class MockCompanyAPI(CompanyAPIInterface):
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.mock_dir = os.path.join(self.base_dir, "mock_data")
        
    def _read_json(self, filename: str) -> Dict[str, Any]:
        path = os.path.join(self.mock_dir, filename)
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_json(self, filename: str, data: Dict[str, Any]):
        path = os.path.join(self.mock_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    async def get_customer(self, customer_id: str) -> Optional[Dict[str, Any]]:
        data = self._read_json("customers.json")
        return data.get(customer_id)

    async def get_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        data = self._read_json("orders.json")
        return data.get(order_id)

    async def create_ticket(self, customer_id: str, issue: str) -> Dict[str, Any]:
        data = self._read_json("tickets.json")
        ticket_id = f"TKT-{len(data) + 1:03d}"
        ticket = {
            "customer_id": customer_id,
            "issue": issue,
            "status": "Open"
        }
        data[ticket_id] = ticket
        self._write_json("tickets.json", data)
        ticket["ticket_id"] = ticket_id
        return ticket

    async def update_ticket(self, ticket_id: str, status: str) -> Optional[Dict[str, Any]]:
        data = self._read_json("tickets.json")
        if ticket_id in data:
            data[ticket_id]["status"] = status
            self._write_json("tickets.json", data)
            ticket = data[ticket_id]
            ticket["ticket_id"] = ticket_id
            return ticket
        return None

class RealCompanyAPI(CompanyAPIInterface):
    async def get_customer(self, customer_id: str) -> Optional[Dict[str, Any]]:
        # TODO: Implement real API call
        pass

    async def get_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        # TODO: Implement real API call
        pass

    async def create_ticket(self, customer_id: str, issue: str) -> Dict[str, Any]:
        # TODO: Implement real API call
        pass

    async def update_ticket(self, ticket_id: str, status: str) -> Optional[Dict[str, Any]]:
        # TODO: Implement real API call
        pass

def get_company_api() -> CompanyAPIInterface:
    if settings.MOCK_MODE:
        return MockCompanyAPI()
    return RealCompanyAPI()
