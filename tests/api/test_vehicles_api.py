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
def test_get_single_vehicle(vehicles_client, test_data):
    vehicle_id = test_data["vehicles"]["valid_vehicle_id"]

    response = vehicles_client.get_vehicle(vehicle_id)

    assert_status_code(response.status_code, 200)

    payload = response.json()
    assert_has_keys(
        payload,
        ["vin", "make", "model", "color", "year", "mileage", "lastServiceDate", "nextServiceDate", "owner"],
    )
    assert payload["vin"] == "1HGBH41JXMN109186"
    assert payload["make"] == "Toyota"
    assert payload["model"] == "Camry"
    assert payload["color"] == "Blue"
    assert payload["year"] == 2020
    assert payload["mileage"] == 15000
    assert payload["lastServiceDate"] == "2023-06-15"
    assert payload["nextServiceDate"] == "2024-06-15"

    owner = payload["owner"]
    assert_has_keys(owner, ["id", "firstName", "lastName", "email", "phoneNumber"])
    assert owner["id"] == 1
    assert owner["firstName"] == "John"
    assert owner["lastName"] == "Doe"
    assert owner["email"] == "john.doe@example.com"
    assert owner["phoneNumber"] == "303-555-1234"

@pytest.mark.api
def test_get_unknown_vehicle_returns_not_found(vehicles_client, test_data):
    vehicle_id = test_data["vehicles"]["invalid_vehicle_id"]

    response = vehicles_client.get_vehicle(vehicle_id)

    assert_status_code(response.status_code, 404)

@pytest.mark.api
def test_create_vehicle(vehicles_client, owners_client):
    # First create a new owner to associate with the vehicle
    owner_response = owners_client.create_owner({
        "firstName": "Test",
        "lastName": "Owner",
        "email": "test.owner@example.com",
        "phoneNumber": "303-555-5678"
    })
    assert_status_code(owner_response.status_code, 201)
    owner = owner_response.json()
    owner_id = owner["id"]

    # Now create a new vehicle associated with the newly created owner
    vehicle_response = vehicles_client.create_vehicle({
        "vin": "1HGBH41JXMN109187",
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
    vehicle = vehicle_response.json()
    assert_has_keys(vehicle, ["vin", "make", "model", "color", "year", "mileage", "lastServiceDate", "nextServiceDate", "ownerId"])
    assert vehicle["vin"] == "1HGBH41JXMN109187"
    assert vehicle["make"] == "Honda"
    assert vehicle["model"] == "Civic"
    assert vehicle["color"] == "Red"
    assert vehicle["year"] == 2021
    assert vehicle["mileage"] == 10000
    assert vehicle["lastServiceDate"] == "2023-07-01"
    assert vehicle["nextServiceDate"] == "2024-07-01"
    assert vehicle["ownerId"] == owner_id