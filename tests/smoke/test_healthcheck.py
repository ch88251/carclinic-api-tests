import pytest

from src.utils.assertions import assert_status_code


@pytest.mark.smoke
def test_owners_endpoint_is_available(owners_client):
    response = owners_client.list_owners()
    assert_status_code(response.status_code, 200)
