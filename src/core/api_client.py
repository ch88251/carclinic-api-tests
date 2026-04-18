from __future__ import annotations

from typing import Any

import requests

from src.core.config import EnvironmentConfig
from src.utils.logger import get_logger


logger = get_logger(__name__)


class ApiClient:
    def __init__(self, config: EnvironmentConfig, session: requests.Session) -> None:
        self.config = config
        self.session = session

    def _build_url(self, path: str) -> str:
        return f"{self.config.base_url.rstrip('/')}/{path.lstrip('/')}"

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        url = self._build_url(path)
        logger.info("GET %s", url)
        response = self.session.get(url, timeout=self.config.timeout, **kwargs)
        return response

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        url = self._build_url(path)
        logger.info("POST %s", url)
        response = self.session.post(url, timeout=self.config.timeout, **kwargs)
        return response

    def put(self, path: str, **kwargs: Any) -> requests.Response:
        url = self._build_url(path)
        logger.info("PUT %s", url)
        response = self.session.put(url, timeout=self.config.timeout, **kwargs)
        return response

    def patch(self, path: str, **kwargs: Any) -> requests.Response:
        url = self._build_url(path)
        logger.info("PATCH %s", url)
        response = self.session.patch(url, timeout=self.config.timeout, **kwargs)
        return response

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        url = self._build_url(path)
        logger.info("DELETE %s", url)
        response = self.session.delete(url, timeout=self.config.timeout, **kwargs)
        return response
