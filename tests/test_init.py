from __future__ import annotations

import types
import unittest

from helpers import load_addon_module, make_mw


class InitModuleTests(unittest.TestCase):
    def test_import_registers_web_exports_and_bootstrap_hooks(self) -> None:
        mw = make_mw()
        calls: dict[str, object] = {}
        package_name = "text_tools_testpkg_init"

        def set_web_exports(module_name: str, pattern: str) -> None:
            calls["set_web_exports"] = (module_name, pattern)

        mw.addonManager.setWebExports = set_web_exports

        fake_config_dialog = types.ModuleType("fake_config_dialog")
        fake_config_dialog.register_config_action = lambda: calls.__setitem__(
            "register_config_action", True
        )

        fake_config_store = types.ModuleType("fake_config_store")
        fake_config_store.migrate_config_if_needed = lambda: calls.__setitem__(
            "migrate_config_if_needed", True
        )

        fake_hooks = types.ModuleType("fake_hooks")
        fake_hooks.register_hooks = lambda: calls.__setitem__("register_hooks", True)

        load_addon_module(
            "__init__",
            mw=mw,
            package_name=package_name,
            extra_modules={
                f"{package_name}.config_dialog": fake_config_dialog,
                f"{package_name}.config_store": fake_config_store,
                f"{package_name}.hooks": fake_hooks,
            },
        )

        self.assertEqual(
            calls["set_web_exports"],
            (f"{package_name}.__init__", r"web/.*\.(js|css)"),
        )
        self.assertTrue(calls["migrate_config_if_needed"])
        self.assertTrue(calls["register_config_action"])
        self.assertTrue(calls["register_hooks"])


if __name__ == "__main__":
    unittest.main()
