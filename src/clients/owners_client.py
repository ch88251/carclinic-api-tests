from __future__ import annotations

from src.core.api_client import ApiClient


class OwnersClient:
    def __init__(self, api_client: ApiClient) -> None:
        self.api_client = api_client

    def get_owner(self, owner_id: int):
        return self.api_client.get(f"/api/owners/{owner_id}")

    def list_owners(self):
        return self.api_client.get("/api/owners")

    def create_owner(self, owner_data: dict):
        return self.api_client.post("/api/owners", json=owner_data)
    
    def delete_owner(self, owner_id: int):
        return self.api_client.delete(f"/api/owners/{owner_id}")