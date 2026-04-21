from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any, Generator

import pytest
import requests
import yaml
from pytest_html import extras as html_extras

from src.clients.vehicles_client import VehiclesClient
from src.clients.owners_client import OwnersClient
from src.core.api_client import ApiClient
from src.core.config import AppConfig, EnvironmentConfig, load_app_configs, load_environment_config
from src.core.response_capture import set_current_log
from src.core.session import create_session
from src.utils.report_extras import format_response_as_html


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_FILE = PROJECT_ROOT / "config" / "config.yaml"
TEST_DATA_FILE = PROJECT_ROOT / "config" / "test_data.yaml"

_RESPONSES_KEY: pytest.StashKey[list[requests.Response]] = pytest.StashKey()


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environment to run tests against (default: dev)",
    )
    parser.addoption(
        "--log-api-details",
        action="store_true",
        default=False,
        help="Include API request/response details in the HTML report for all tests (default: failed tests only)",
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

@pytest.fixture(scope="session")
def vehicles_client(env_config: EnvironmentConfig, app_configs: dict[str, AppConfig]) -> VehiclesClient:
    config = replace(env_config, base_url=env_config.url_for_app(app_configs["carclinic"]))
    session = create_session(config)
    return VehiclesClient(ApiClient(config=config, session=session))


@pytest.fixture(autouse=True)
def _capture_api_calls(request: pytest.FixtureRequest) -> Generator[None, None, None]:
    log: list = []
    request.node.stash[_RESPONSES_KEY] = log
    set_current_log(log)
    yield
    set_current_log(None)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> Generator[None, None, None]:
    outcome = yield
    report = outcome.get_result()

    if call.when != "call":
        return

    log_all = item.config.getoption("--log-api-details", default=False)
    if not (report.failed or log_all):
        return

    responses = item.stash.get(_RESPONSES_KEY, [])
    if not responses:
        return

    extras = getattr(report, "extras", [])
    for response in responses:
        extras.append(html_extras.html(format_response_as_html(response)))
    report.extras = extras
