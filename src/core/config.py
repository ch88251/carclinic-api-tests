from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class AppConfig:
    name: str
    port: int


@dataclass
class EnvironmentConfig:
    name: str
    base_url: str
    timeout: int = 10
    verify_ssl: bool = True
    headers: dict[str, str] = field(default_factory=dict)

    def url_for_app(self, app: AppConfig) -> str:
        return f"{self.base_url.rstrip('/')}:{app.port}"


def load_yaml(file_path: str | Path) -> dict[str, Any]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    if not isinstance(data, dict):
        raise ValueError(f"Invalid YAML structure in {path}")
    return data


def load_environment_config(env_name: str, file_path: str | Path) -> EnvironmentConfig:
    data = load_yaml(file_path)
    environments = data.get("environments", {})
    env_data = environments.get(env_name)

    if not isinstance(env_data, dict):
        available = ", ".join(sorted(environments.keys()))
        raise KeyError(
            f"Environment '{env_name}' not found in {file_path}. "
            f"Available environments: {available}"
        )

    return EnvironmentConfig(
        name=env_name,
        base_url=env_data["base_url"],
        timeout=env_data.get("timeout", 10),
        verify_ssl=env_data.get("verify_ssl", True),
        headers=env_data.get("headers", {}),
    )


def load_app_configs(file_path: str | Path) -> dict[str, AppConfig]:
    data = load_yaml(file_path)
    apps = data.get("apps", {})

    if not isinstance(apps, dict):
        raise ValueError(f"Invalid 'apps' section in {file_path}")

    return {
        name: AppConfig(name=name, port=int(app_data["port"]))
        for name, app_data in apps.items()
        if isinstance(app_data, dict) and "port" in app_data
    }
