from __future__ import annotations

from src.core.api_client import ApiClient


class StaffClient:
    def __init__(self, api_client: ApiClient) -> None:
        self.api_client = api_client

    def get_staff_member(self, staff_id: int):
        return self.api_client.get(f"/api/staff/{staff_id}")

    def list_staff_members(self):
        return self.api_client.get("/api/staff")

    def create_staff_member(self, staff_data: dict):
        return self.api_client.post("/api/staff", json=staff_data)
    
    def delete_staff_member(self, staff_id: int):
        return self.api_client.delete(f"/api/staff/{staff_id}")