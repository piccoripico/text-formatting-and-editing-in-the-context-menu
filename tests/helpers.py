from __future__ import annotations

import importlib.util
import sys
import types
import uuid
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ADDON_ROOT = REPO_ROOT / "Text-Tools"
SCRIPTS_ROOT = REPO_ROOT / "scripts"


class FakeAddonManager:
    def __init__(self, config: dict | None = None) -> None:
        self._config = config
        self.write_calls: list[tuple[str, dict]] = []

    def getConfig(self, addon_module: str) -> dict | None:
        return self._config

    def writeConfig(self, addon_module: str, config: dict) -> None:
        self.write_calls.append((addon_module, config))
        self._config = config


def make_mw(config: dict | None = None) -> types.SimpleNamespace:
    return types.SimpleNamespace(addonManager=FakeAddonManager(config))


def load_addon_module(module_basename: str, *, mw: types.SimpleNamespace | None = None):
    fake_aqt = types.ModuleType("aqt")
    fake_aqt.mw = mw if mw is not None else make_mw()
    sys.modules["aqt"] = fake_aqt

    package_name = f"text_tools_testpkg_{uuid.uuid4().hex}"
    package = types.ModuleType(package_name)
    package.__path__ = [str(ADDON_ROOT)]
    package.__file__ = str(ADDON_ROOT / "__init__.py")
    sys.modules[package_name] = package

    return _load_module(
        f"{package_name}.{module_basename}",
        ADDON_ROOT / f"{module_basename}.py",
    )


def load_script_module(script_filename: str):
    script_path = SCRIPTS_ROOT / script_filename
    module_name = f"script_testpkg_{uuid.uuid4().hex}_{script_path.stem}"
    return _load_module(module_name, script_path)


def _load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec for {file_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
