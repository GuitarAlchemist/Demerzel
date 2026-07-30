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
        if not isinstance(cfg.get("adapter"), str) or not cfg["adapter"].strip():
            raise RegistryError(f"{p}: backend {name!r} missing required adapter")

        from_config = cfg.get("provider_from_config", False)
        if not isinstance(from_config, bool):
            raise RegistryError(
                f"{p}: backend {name!r} provider_from_config must be a boolean")
        if from_config:
            if "provider" in cfg:
                raise RegistryError(
                    f"{p}: backend {name!r} sets both provider and "
                    f"provider_from_config; the attribution has one source")
        elif not isinstance(cfg.get("provider"), str) or not cfg["provider"].strip():
            raise RegistryError(f"{p}: backend {name!r} missing required provider")

        if "enabled" not in cfg:
            cfg["enabled"] = False
        elif not isinstance(cfg["enabled"], bool):
            raise RegistryError(f"{p}: backend {name!r} enabled must be a boolean")

        # A backend whose spend attribution depends on operator configuration
        # cannot be enabled without stating what it bills. Hardcoding a guess in
        # the registry is how a metered endpoint ends up gated as a free
        # local-seat subscription (#915, same shape as #863).
        if from_config and cfg["enabled"] and _config_provider(cfg) is None:
            raise RegistryError(
                f"{p}: backend {name!r} is enabled but its config block declares "
                f"no provider; set config.provider to the allowlisted AIW provider "
                f"this backend actually bills")

    return backends


def _config_provider(cfg: dict[str, Any]) -> str | None:
    """Return the provider declared inside a backend's own config block, if any."""
    conf = cfg.get("config")
    if not isinstance(conf, dict):
        return None
    value = conf.get("provider")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


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
    return cls(cfg.get("config"))


def provider_for(name: str, registry: dict[str, dict[str, Any]] | None = None) -> str:
    """Return the AIW budget provider id for the named backend.

    For a backend marked ``provider_from_config``, the attribution is a property
    of the endpoint an operator configured, not of the adapter, so it is read
    from ``config.provider``. An unset one raises rather than falling back to a
    default: the caller (``_budget_reserve``) fails closed on the raise, whereas
    a fallback would bill metered spend under whatever the default happened to
    be (#915).
    """
    reg = load_registry() if registry is None else registry
    cfg = reg.get(name)
    if cfg is None:
        raise RegistryError(f"unknown backend {name!r}")
    if cfg.get("provider_from_config"):
        provider = _config_provider(cfg)
        if provider is None:
            raise RegistryError(
                f"backend {name!r} takes its budget provider from its config "
                f"block and none is set; there is no safe default to assume")
        return provider
    return cfg["provider"]
