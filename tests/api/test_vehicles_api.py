import pytest

from src.utils.assertions import assert_has_count, assert_has_keys, assert_status_code

@pytest.mark.api
def test_get_all_vehicles(vehicles_client):
    response = vehicles_client.list_vehicles()

    assert_status_code(response.status_code, 200)

    payload = response.json()
    assert isinstance(payload, list)
    if payload:
        assert_has_keys(
            payload[0],
            ["vin", "make", "model", "color", "year", "mileage", "lastServiceDate", "nextServiceDate"],
        )

@pytest.mark.api
def test_create_vehicle(vehicles_client, owners_client):
    # First create a new owner to associate with the vehicle
    owner_response = owners_client.create_owner({
        "firstName": "ghghghg",
        "lastName": "tytytr",
        "email": "test.owner@example.com",
        "phoneNumber": "303-555-5678"
    })
    assert_status_code(owner_response.status_code, 201)
    owner = owner_response.json()
    owner_id = owner["id"]

    # Now create a new vehicle associated with the newly created owner
    vehicle_response = vehicles_client.create_vehicle({
        "vin": "AAAAB1111BBBB2222",
        "make": "Honda",
        "model": "Civic",
        "color": "Red",
        "year": 2021,
        "mileage": 10000,
        "lastServiceDate": "2023-07-01",
        "nextServiceDate": "2024-07-01",
        "ownerId": owner_id
    })
    assert_status_code(vehicle_response.status_code, 201)

    # Now delete the vehicle
    vehicle_id = vehicle_response.json()["id"]
    vehicles_client.delete_vehicle(vehicle_id)

