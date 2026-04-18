from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest
import yaml

from src.clients.owners_client import OwnersClient
from src.core.api_client import ApiClient
from src.core.config import AppConfig, EnvironmentConfig, load_app_configs, load_environment_config
from src.core.session import create_session


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_FILE = PROJECT_ROOT / "config" / "config.yaml"
TEST_DATA_FILE = PROJECT_ROOT / "config" / "test_data.yaml"


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environment to run tests against (default: dev)",
    )


@pytest.fixture(scope="session")
def env_name(pytestconfig: pytest.Config) -> str:
    return str(pytestconfig.getoption("--env"))


@pytest.fixture(scope="session")
def env_config(env_name: str) -> EnvironmentConfig:
    return load_environment_config(env_name, CONFIG_FILE)


@pytest.fixture(scope="session")
def app_configs() -> dict[str, AppConfig]:
    return load_app_configs(CONFIG_FILE)


@pytest.fixture(scope="session")
def test_data() -> dict[str, Any]:
    with TEST_DATA_FILE.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


@pytest.fixture(scope="session")
def api_client(env_config: EnvironmentConfig) -> ApiClient:
    session = create_session(env_config)
    return ApiClient(config=env_config, session=session)


@pytest.fixture(scope="session")
def owners_client(env_config: EnvironmentConfig, app_configs: dict[str, AppConfig]) -> OwnersClient:
    config = replace(env_config, base_url=env_config.url_for_app(app_configs["carclinic"]))
    session = create_session(config)
    return OwnersClient(ApiClient(config=config, session=session))
