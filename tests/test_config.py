import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


CONFIG_KEYS = ("MONGO_URL", "DATABASE", "REPORT_TOKEN", "ALLOWED_ORIGINS")


@pytest.fixture
def config_path(tmp_path):
    app_directory = tmp_path / "app"
    app_directory.mkdir()
    source = Path(__file__).resolve().parents[1] / "app" / "config.py"
    target = app_directory / "config.py"
    shutil.copyfile(source, target)
    return target


def read_config(config_path, variables=None):
    environment = os.environ.copy()
    for name in (*CONFIG_KEYS, "PYTHON_DOTENV_DISABLED"):
        environment.pop(name, None)
    environment.update(variables or {})

    working_directory = config_path.parent.parent / "another_directory"
    working_directory.mkdir()
    result = subprocess.run(
        [
            sys.executable,
            "-B",
            "-c",
            "import json, runpy, sys; "
            "config = runpy.run_path(sys.argv[1]); "
            f"print(json.dumps({{name: config[name] for name in {CONFIG_KEYS!r}}}))",
            str(config_path),
        ],
        cwd=working_directory,
        env=environment,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def test_defaults_without_env_file_or_environment_variables(config_path):
    assert read_config(config_path) == {
        "MONGO_URL": "mongodb://localhost:27017",
        "DATABASE": "ada_exam",
        "REPORT_TOKEN": "demo-only-not-a-real-secret",
        "ALLOWED_ORIGINS": ["http://localhost:4200"],
    }


def test_loads_project_env_file_from_another_working_directory(config_path):
    env_path = config_path.parent.parent / ".env"
    env_path.write_text(
        'MONGO_URL=" mongodb://dotenv-host:27017 "\n'
        'DATABASE=" dotenv_database "\n'
        'REPORT_TOKEN=" dotenv-demo-token "\n'
        "ALLOWED_ORIGINS=http://localhost:4200, https://dashboard.example.com, ,\n",
        encoding="utf-8-sig",
    )

    assert read_config(config_path) == {
        "MONGO_URL": "mongodb://dotenv-host:27017",
        "DATABASE": "dotenv_database",
        "REPORT_TOKEN": "dotenv-demo-token",
        "ALLOWED_ORIGINS": [
            "http://localhost:4200",
            "https://dashboard.example.com",
        ],
    }


def test_environment_variables_take_precedence_over_env_file(config_path):
    env_path = config_path.parent.parent / ".env"
    env_path.write_text(
        "MONGO_URL=mongodb://dotenv-host:27017\n"
        "DATABASE=dotenv_database\n"
        "REPORT_TOKEN=dotenv-demo-token\n"
        "ALLOWED_ORIGINS=http://localhost:4200\n",
        encoding="utf-8",
    )

    assert read_config(config_path, {
        "MONGO_URL": "mongodb://environment-host:27017",
        "DATABASE": "environment_database",
        "REPORT_TOKEN": "environment-demo-token",
        "ALLOWED_ORIGINS": "https://production.example.com",
    }) == {
        "MONGO_URL": "mongodb://environment-host:27017",
        "DATABASE": "environment_database",
        "REPORT_TOKEN": "environment-demo-token",
        "ALLOWED_ORIGINS": ["https://production.example.com"],
    }
