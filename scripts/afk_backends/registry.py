#!/usr/bin/env python3
"""Backend registry loader for the AFK implement lane.

The registry maps backend names to adapter classes and AIW budget providers. It
lives in config/afk-backends.yaml so that new tools, providers, and cost
attributions can be added without editing the governor.
"""
from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

import yaml

from afk_backends import AFKBackend


CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "afk-backends.yaml"


class RegistryError(ValueError):
    """The backend registry is missing, malformed, or names an unknown adapter."""


def load_registry(path: Path | None = None) -> dict[str, dict[str, Any]]:
    """Load the backend registry from YAML.

    Returns a dict keyed by backend name. Raises RegistryError on any problem so
    the governor fails closed.
    """
    p = path or CONFIG_PATH
    try:
        with p.open(encoding="utf-8") as stream:
            data = yaml.safe_load(stream)
    except (OSError, yaml.YAMLError) as exc:
        raise RegistryError(f"could not load backend registry from {p}: {exc}") from exc

    if not isinstance(data, dict) or data.get("schema_version") != "1.0":
        raise RegistryError(f"{p}: expected schema_version '1.0'")
    backends = data.get("backends")
    if not isinstance(backends, dict) or not backends:
        raise RegistryError(f"{p}: missing or empty 'backends' section")

    for name, cfg in backends.items():
        if not isinstance(cfg, dict):
            raise RegistryError(f"{p}: backend {name!r} must be a mapping")
        for key in ("adapter", "provider"):
            if not isinstance(cfg.get(key), str) or not cfg[key].strip():
                raise RegistryError(f"{p}: backend {name!r} missing required {key}")
        if "enabled" not in cfg:
            cfg["enabled"] = False
        elif not isinstance(cfg["enabled"], bool):
            raise RegistryError(f"{p}: backend {name!r} enabled must be a boolean")

    return backends


def _resolve_class(dotted_path: str) -> type[AFKBackend]:
    """Import a dotted class path and verify it is an AFKBackend subclass."""
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as exc:
        raise RegistryError(f"adapter path must be dotted.module.ClassName: {dotted_path}") from exc
    try:
        module = importlib.import_module(module_path)
    except ImportError as exc:
        raise RegistryError(f"could not import adapter module {module_path}: {exc}") from exc
    cls = getattr(module, class_name, None)
    if not isinstance(cls, type):
        raise RegistryError(f"adapter {dotted_path} is not a class")
    if not issubclass(cls, AFKBackend):
        raise RegistryError(f"adapter {dotted_path} does not implement AFKBackend")
    return cls


def get_backend(name: str, registry: dict[str, dict[str, Any]] | None = None) -> AFKBackend:
    """Return an adapter instance for the named backend.

    Raises RegistryError if the backend is unknown, disabled, or misconfigured.
    """
    reg = load_registry() if registry is None else registry
    cfg = reg.get(name)
    if cfg is None:
        raise RegistryError(f"unknown backend {name!r}")
    if not cfg.get("enabled", False):
        raise RegistryError(f"backend {name!r} is disabled in the registry")
    cls = _resolve_class(cfg["adapter"])
    return cls()


def provider_for(name: str, registry: dict[str, dict[str, Any]] | None = None) -> str:
    """Return the AIW budget provider id for the named backend."""
    reg = load_registry() if registry is None else registry
    cfg = reg.get(name)
    if cfg is None:
        raise RegistryError(f"unknown backend {name!r}")
    return cfg["provider"]
