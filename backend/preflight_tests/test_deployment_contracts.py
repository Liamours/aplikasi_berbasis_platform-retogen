import json
import re
import tomllib
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_DIR.parent


def read_repo_file(*parts: str) -> str:
    return (REPO_ROOT.joinpath(*parts)).read_text(encoding="utf-8")


def test_backend_dockerfile_installs_production_dependencies_only():
    dockerfile = read_repo_file("backend", "Dockerfile")

    assert "uv sync --frozen --no-dev" in dockerfile


def test_backend_dockerfile_runtime_does_not_sync_dependencies():
    dockerfile = read_repo_file("backend", "Dockerfile")

    assert re.search(r"^CMD\s+uv run --no-sync uvicorn main:app", dockerfile, re.MULTILINE)
    assert not re.search(r"^CMD\s+uv run uvicorn main:app", dockerfile, re.MULTILINE)


def test_backend_dockerfile_chowns_app_before_non_root_user():
    lines = read_repo_file("backend", "Dockerfile").splitlines()

    chown_index = next(
        index for index, line in enumerate(lines)
        if "chown -R appuser:appuser /app" in line
    )
    user_index = next(
        index for index, line in enumerate(lines)
        if line.strip() == "USER appuser"
    )

    assert chown_index < user_index


def test_backend_railway_config_uses_dockerfile_and_root_healthcheck():
    config = json.loads(read_repo_file("backend", "railway.json"))

    assert config["build"]["builder"].upper() == "DOCKERFILE"
    assert config["build"]["dockerfilePath"] == "Dockerfile"
    assert config["deploy"]["healthcheckPath"] == "/"


def test_frontend_railway_config_uses_dockerfile_and_root_healthcheck():
    config = tomllib.loads(read_repo_file("frontend", "railway.toml"))

    assert config["build"]["builder"].upper() == "DOCKERFILE"
    assert config["build"]["dockerfilePath"] == "Dockerfile"
    assert config["deploy"]["healthcheckPath"] == "/"


def test_frontend_dockerfile_uses_node_22_runtime():
    dockerfile = read_repo_file("frontend", "Dockerfile")

    assert "FROM node:22-alpine AS builder" in dockerfile
    assert "FROM node:22-alpine AS runner" in dockerfile


def test_frontend_runtime_config_uses_static_public_api_base_default():
    nuxt_config = read_repo_file("frontend", "nuxt.config.ts")

    assert "process.env.NUXT_PUBLIC_API_BASE" not in nuxt_config
    assert "apiBase: 'http://localhost:8000'" in nuxt_config
    assert "apiBase" in nuxt_config


def test_backend_exposes_database_health_endpoint():
    main_py = read_repo_file("backend", "main.py")

    assert '@app.get("/health")' in main_py
    assert 'await db.command("ping")' in main_py


def test_backend_indexes_include_notification_ttl_index():
    indexes_py = read_repo_file("backend", "db", "indexes.py")

    assert "notification_created_ttl" in indexes_py
    assert "expireAfterSeconds=NOTIFICATION_TTL_SECONDS" in indexes_py
    assert "logger.exception" in indexes_py
    assert "raise" in indexes_py


def test_preflight_checks_docker_and_database_health_endpoint():
    script = read_repo_file("scripts", "deployment-preflight.ps1")

    assert "docker info" in script
    assert "http://localhost:8000/health" in script
