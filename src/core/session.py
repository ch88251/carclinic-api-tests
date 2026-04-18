from __future__ import annotations

import requests

from src.core.config import EnvironmentConfig


def create_session(config: EnvironmentConfig) -> requests.Session:
    session = requests.Session()
    session.verify = config.verify_ssl
    session.headers.update(config.headers)
    return session
