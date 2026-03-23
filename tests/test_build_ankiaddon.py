from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock
from zipfile import ZipFile

from helpers import load_script_module


class BuildAnkiaddonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_script_module("build_ankiaddon.py")

    def test_should_include_filters_generated_and_user_specific_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            addon_root = Path(tmp_dir) / "Text-Tools"
            with mock.patch.object(self.module, "ADDON_ROOT", addon_root):
                self.assertFalse(
                    self.module.should_include(addon_root / "__pycache__" / "module.py")
                )
                self.assertFalse(self.module.should_include(addon_root / "module.pyc"))
                self.assertFalse(
                    self.module.should_include(addon_root / "user_files" / "private.txt")
                )
                self.assertTrue(
                    self.module.should_include(addon_root / "user_files" / "README.txt")
                )
                self.assertTrue(self.module.should_include(addon_root / "web" / "commands.js"))

    def test_build_package_writes_a_clean_archive_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            addon_root = root / "Text-Tools"
            (addon_root / "__pycache__").mkdir(parents=True)
            (addon_root / "user_files").mkdir(parents=True)
            (addon_root / "web").mkdir(parents=True)

            (addon_root / "__init__.py").write_text("# init\n", encoding="utf-8")
            (addon_root / "config.json").write_text("{}\n", encoding="utf-8")
            (addon_root / "__pycache__" / "ignored.pyc").write_bytes(b"cache")
            (addon_root / "user_files" / "README.txt").write_text("keep\n", encoding="utf-8")
            (addon_root / "user_files" / "private.txt").write_text("drop\n", encoding="utf-8")
            (addon_root / "web" / "commands.js").write_text(
                "console.log('ok');\n",
                encoding="utf-8",
            )

            output_path = root / "dist" / "Text-Tools.ankiaddon"

            with mock.patch.object(self.module, "ADDON_ROOT", addon_root):
                packaged_files = self.module.build_package(output_path)

            packaged_names = [path.as_posix() for path in packaged_files]
            self.assertEqual(
                packaged_names,
                ["__init__.py", "config.json", "user_files/README.txt", "web/commands.js"],
            )

            with ZipFile(output_path) as archive:
                self.assertEqual(
                    sorted(archive.namelist()),
                    ["__init__.py", "config.json", "user_files/README.txt", "web/commands.js"],
                )


if __name__ == "__main__":
    unittest.main()
