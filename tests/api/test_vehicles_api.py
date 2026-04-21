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