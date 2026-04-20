from __future__ import annotations

import threading

import requests


_local = threading.local()


def get_current_log() -> list[requests.Response] | None:
    return getattr(_local, "log", None)


def set_current_log(log: list[requests.Response] | None) -> None:
    _local.log = log


def capture_response(response: requests.Response, *args: object, **kwargs: object) -> requests.Response:
    log = get_current_log()
    if log is not None:
        log.append(response)
    return response
