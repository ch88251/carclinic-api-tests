from __future__ import annotations

import requests

from src.core.config import EnvironmentConfig
from src.core.response_capture import capture_response


def create_session(config: EnvironmentConfig) -> requests.Session:
    session = requests.Session()
    session.verify = config.verify_ssl
    session.headers.update(config.headers)
    session.hooks["response"].append(capture_response)
    return session
