import pytest

from src.utils.assertions import assert_has_count, assert_has_keys, assert_status_code

def test_get_all_owners(owners_client):
    response = owners_client.list_owners()

    assert_status_code(response.status_code, 200)

    payload = response.json()
    assert isinstance(payload, list)
    if payload:
        assert_has_keys(
            payload[0],
            ["id", "firstName", "lastName", "email", "phoneNumber"],
        )

def test_create_owner(owners_client):
    response = owners_client.create_owner({
        "firstName": "Test",
        "lastName": "Owner",
        "email": "test.owner@example.com",
        "phoneNumber": "555-1234"
    })

    assert_status_code(response.status_code, 201)
    payload = response.json()
    assert_has_keys(
        payload,
        ["id", "firstName", "lastName", "email", "phoneNumber"],
    )
    assert payload["firstName"] == "Test"
    assert payload["lastName"] == "Owner"
    assert payload["email"] == "test.owner@example.com"
    assert payload["phoneNumber"] == "555-1234"

def test_delete_owner(owners_client, test_data):
    # First create a new owner to ensure we have a valid ID to delete
    create_response = owners_client.create_owner({
        "firstName": "Delete",
        "lastName": "Me",
        "email": "delete.me@example.com",
        "phoneNumber": "555-0000"
    })
    assert_status_code(create_response.status_code, 201)
    owner_id = create_response.json()["id"]

    # Now delete the owner
    delete_response = owners_client.delete_owner(owner_id)
    assert_status_code(delete_response.status_code, 204)
