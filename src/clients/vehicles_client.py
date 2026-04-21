from __future__ import annotations

from src.core.api_client import ApiClient

class VehiclesClient:
    def __init__(self, api_client: ApiClient) -> None:
        self.api_client = api_client

    def get_vehicle(self, vehicle_id: int):
        return self.api_client.get(f"/api/vehicles/{vehicle_id}")

    def list_vehicles(self):
        return self.api_client.get("/api/vehicles")

    def create_vehicle(self, vehicle_data: dict):
        return self.api_client.post("/api/vehicles", json=vehicle_data)
    
    def delete_vehicle(self, vehicle_id: int):
        return self.api_client.delete(f"/api/vehicles/{vehicle_id}")