from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from helpers import load_addon_module, make_mw


class ConfigStoreTests(unittest.TestCase):
    def test_load_config_merges_defaults_and_normalizes_values(self) -> None:
        current = {
            "editor": {"enabled": 0},
            "reviewer": "invalid",
            "selected_quick_access_items": [
                "backRed",
                "Highlight Red",
                "Ruby",
                "Insert Horizontal Line",
                "Ruby",
            ],
            "quick_access_position": 1,
            "user_words_flag": 0,
            "user_words": [" Alpha ", "Beta", "Alpha", ""],
            "user_words_position": "yes",
            "custom_flag": "keep me",
        }
        module = load_addon_module("config_store", mw=make_mw(current))

        loaded = module.load_config()

        self.assertEqual(
            loaded["selected_quick_access_items"],
            ["Highlight Red", "Insert Ruby", "Horizontal Line"],
        )
        self.assertEqual(loaded["user_words"], ["Alpha", "Beta"])
        self.assertFalse(loaded["editor"]["enabled"])
        self.assertTrue(loaded["reviewer"]["enabled"])
        self.assertTrue(loaded["quick_access_position"])
        self.assertFalse(loaded["user_words_flag"])
        self.assertTrue(loaded["user_words_position"])
        self.assertEqual(loaded["custom_flag"], "keep me")
        self.assertEqual(loaded["config_version"], module.CONFIG_VERSION)

    def test_migrate_config_creates_backup_and_writes_normalized_config_once(self) -> None:
        current = {
            "editor": None,
            "selected_quick_access_items": ["Ruby", "Insert Horizontal Line", "Ruby"],
            "user_words": [" One ", "Two", "One"],
        }
        mw = make_mw(current)
        module = load_addon_module("config_store", mw=mw)

        with tempfile.TemporaryDirectory() as tmp_dir:
            addon_root = Path(tmp_dir)
            with mock.patch.object(module, "_addon_root", return_value=addon_root):
                module.migrate_config_if_needed()
                module.migrate_config_if_needed()

            backup_path = addon_root / "user_files" / "config-backup-v1.json"
            self.assertTrue(backup_path.exists())
            self.assertEqual(json.loads(backup_path.read_text(encoding="utf-8")), current)

        self.assertEqual(len(mw.addonManager.write_calls), 1)
        addon_module, written_config = mw.addonManager.write_calls[0]
        self.assertEqual(addon_module, module.ADDON_MODULE)
        self.assertEqual(
            written_config["selected_quick_access_items"],
            ["Insert Ruby", "Horizontal Line"],
        )
        self.assertEqual(written_config["user_words"], ["One", "Two"])

    def test_migrate_config_noops_when_config_is_already_normalized(self) -> None:
        module = load_addon_module("config_store")
        current = json.loads(json.dumps(module.DEFAULT_CONFIG))
        mw = make_mw(current)
        module = load_addon_module("config_store", mw=mw)

        with tempfile.TemporaryDirectory() as tmp_dir:
            addon_root = Path(tmp_dir)
            with mock.patch.object(module, "_addon_root", return_value=addon_root):
                module.migrate_config_if_needed()

            self.assertFalse((addon_root / "user_files" / "config-backup-v1.json").exists())

        self.assertEqual(mw.addonManager.write_calls, [])


if __name__ == "__main__":
    unittest.main()
