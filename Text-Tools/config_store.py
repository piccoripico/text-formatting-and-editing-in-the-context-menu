from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from aqt import mw

ADDON_MODULE = __name__.split(".")[0]
CONFIG_VERSION = 2

DEFAULT_CONFIG: dict[str, Any] = {
    "config_version": CONFIG_VERSION,
    "editor": {"enabled": True},
    "reviewer": {"enabled": True},
    "selected_quick_access_items": [],
    "quick_access_position": False,
    "user_words_flag": True,
    "user_words": [],
    "user_words_position": False,
}

LEGACY_QUICK_ACCESS_LABEL_ALIASES: dict[str, str] = {
    "(Clear Format)": "Clear All Formatting",
    "backRed": "Highlight Red",
    "backGreen": "Highlight Green",
    "backBlue": "Highlight Blue",
    "backCyan": "Highlight Cyan",
    "backMagenta": "Highlight Magenta",
    "backYellow": "Highlight Yellow",
    "backBlack": "Highlight Black",
    "backWhite": "Highlight White",
    "Size 1": "X-Small",
    "Size 2": "Small",
    "Size 3": "Medium",
    "Size 4": "Large",
    "Size 5": "X-Large",
    "Size 6": "XX-Large",
    "Size 7": "XXX-Large",
    "Ruby": "Insert Ruby",
    "Insert Blockquote": "Blockquote",
    "Insert Horizontal Line": "Horizontal Line",
}


def _addon_root() -> Path:
    return Path(__file__).resolve().parent


def _user_files_dir() -> Path:
    path = _addon_root() / "user_files"
    path.mkdir(exist_ok=True)
    return path


def _deep_fill(defaults: Any, current: Any) -> Any:
    if isinstance(defaults, dict):
        current = current if isinstance(current, dict) else {}
        merged: dict[str, Any] = {}
        for key, default_value in defaults.items():
            merged[key] = _deep_fill(default_value, current.get(key))
        for key, value in current.items():
            if key not in merged:
                merged[key] = value
        return merged
    return defaults if current is None else current


def _dedupe_keep_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        text = str(value).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    return result


def _normalize_quick_access_labels(values: list[str]) -> list[str]:
    migrated = [LEGACY_QUICK_ACCESS_LABEL_ALIASES.get(value, value) for value in values]
    return _dedupe_keep_order(migrated)


def normalize_config(config: dict[str, Any]) -> dict[str, Any]:
    editor = config.get("editor")
    reviewer = config.get("reviewer")

    config["editor"] = editor if isinstance(editor, dict) else {}
    config["reviewer"] = reviewer if isinstance(reviewer, dict) else {}

    config["editor"]["enabled"] = bool(config["editor"].get("enabled", True))
    config["reviewer"]["enabled"] = bool(config["reviewer"].get("enabled", True))

    selected_quick_access_items = config.get("selected_quick_access_items", [])
    if not isinstance(selected_quick_access_items, list):
        selected_quick_access_items = []
    config["selected_quick_access_items"] = _normalize_quick_access_labels(
        [str(x) for x in selected_quick_access_items]
    )

    config["quick_access_position"] = bool(config.get("quick_access_position", False))
    config["user_words_flag"] = bool(config.get("user_words_flag", True))

    user_words = config.get("user_words", [])
    if not isinstance(user_words, list):
        user_words = []
    config["user_words"] = _dedupe_keep_order([str(x) for x in user_words])

    config["user_words_position"] = bool(config.get("user_words_position", False))
    config["config_version"] = CONFIG_VERSION
    return config


def load_config() -> dict[str, Any]:
    current = mw.addonManager.getConfig(ADDON_MODULE) or {}
    merged = _deep_fill(copy.deepcopy(DEFAULT_CONFIG), current)
    return normalize_config(merged)


def save_config(config: dict[str, Any]) -> None:
    mw.addonManager.writeConfig(ADDON_MODULE, normalize_config(config))


def _backup_config_once(config: dict[str, Any]) -> None:
    if not config:
        return
    backup_path = _user_files_dir() / "config-backup-v1.json"
    if backup_path.exists():
        return
    backup_path.write_text(
        json.dumps(config, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def migrate_config_if_needed() -> None:
    current = mw.addonManager.getConfig(ADDON_MODULE) or {}
    migrated = normalize_config(_deep_fill(copy.deepcopy(DEFAULT_CONFIG), current))
    if current != migrated:
        _backup_config_once(current)
        save_config(migrated)
