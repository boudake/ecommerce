import os
import re
from pathlib import Path

import yaml


VARIABLE_PATTERN = re.compile(r"\$\{([^}:]+)(?::([^}]+))?\}")


def load_config(
    path: str = "config/application.yaml",
) -> dict:

    config_path = Path(path)

    with config_path.open(
        encoding="utf-8"
    ) as file:
        raw_config = yaml.safe_load(file)

    default_environment = raw_config["app"]["environment"]
    if isinstance(default_environment, str):
        match = VARIABLE_PATTERN.fullmatch(default_environment)
        if match and match.group(1) == "APP_ENV":
            default_environment = match.group(2) or "local"

    environment = os.getenv(
        "APP_ENV",
        default_environment,
    )

    if environment not in {"local", "databricks"}:
        raise ValueError(
            f"Unsupported environment: {environment}"
        )

    raw_config["app"]["environment"] = environment

    config = _resolve_environment(
        raw_config,
        environment,
    )

    return config


def _resolve_environment(
    config: dict,
    environment: str,
) -> dict:

    selected = {
        "app": config["app"],
        "common": config["common"],
        "spark": config[environment]["spark"],
        "paths": config[environment]["paths"],
        "database": config[environment]["database"],
        "datasets": {},
    }

    if environment == "databricks":
        selected["catalog"] = config["databricks"]["catalog"]

    for name, dataset in config["datasets"].items():

        selected["datasets"][name] = {
            **config["common"]["datasets"][name],
            **dataset[environment],
        }

    context = {**config, **selected}
    return _resolve_variables(selected, context)


def _resolve_variables(
    value,
    config,
):
    if isinstance(value, dict):
        return {
            key: _resolve_variables(item, config)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            _resolve_variables(item, config)
            for item in value
        ]

    if isinstance(value, str):

        def replace(match):

            path = match.group(1).split(".")

            current = config

            for part in path:
                current = current[part]

            return str(current)

        return VARIABLE_PATTERN.sub(
            replace,
            value,
        )

    return value