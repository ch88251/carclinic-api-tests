from __future__ import annotations

from typing import Any


def assert_status_code(actual: int, expected: int) -> None:
    assert actual == expected, f"Expected status code {expected}, but got {actual}"


def assert_has_keys(payload: dict[str, Any], expected_keys: list[str]) -> None:
    missing_keys = [key for key in expected_keys if key not in payload]
    assert not missing_keys, f"Response missing keys: {missing_keys}"

def assert_has_count(payload: list[Any], expected_count: int) -> None:
    actual_count = len(payload)
    assert actual_count == expected_count, f"Expected {expected_count} items, but got {actual_count}"