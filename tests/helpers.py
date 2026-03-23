from __future__ import annotations

import importlib.util
import sys
import types
import uuid
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ADDON_ROOT = REPO_ROOT / "Text-Tools"
SCRIPTS_ROOT = REPO_ROOT / "scripts"


class FakeSignal:
    def __init__(self) -> None:
        self._callbacks: list = []

    def connect(self, callback) -> None:
        self._callbacks.append(callback)

    def emit(self, *args, **kwargs) -> None:
        for callback in self._callbacks:
            callback(*args, **kwargs)


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


class FakeAction:
    def __init__(self, text: str, parent=None) -> None:
        self._text = text
        self._parent = parent
        self._menu = None
        self.triggered = FakeSignal()
        self.is_separator = False

    def text(self) -> str:
        return self._text

    def menu(self):
        return self._menu

    def setMenu(self, menu) -> None:
        self._menu = menu


class FakeMenu:
    def __init__(self, title: str = "") -> None:
        self._title = title
        self._actions: list[FakeAction] = []

    def title(self) -> str:
        return self._title

    def actions(self) -> list[FakeAction]:
        return self._actions

    def addAction(self, action: FakeAction) -> FakeAction:
        self._actions.append(action)
        return action

    def addMenu(self, title: str):
        submenu = FakeMenu(title)
        action = FakeAction(title, self)
        action.setMenu(submenu)
        self._actions.append(action)
        return submenu

    def addSeparator(self):
        action = FakeAction("", self)
        action.is_separator = True
        self._actions.append(action)
        return action


class FakeMimeData:
    def __init__(self) -> None:
        self._html = ""
        self._text = ""

    def setHtml(self, value: str) -> None:
        self._html = value

    def setText(self, value: str) -> None:
        self._text = value

    def hasHtml(self) -> bool:
        return bool(self._html)

    def html(self) -> str:
        return self._html

    def text(self) -> str:
        return self._text


class FakeClipboard:
    def __init__(self) -> None:
        self._mime = FakeMimeData()

    def setMimeData(self, mime: FakeMimeData) -> None:
        self._mime = mime

    def mimeData(self) -> FakeMimeData:
        return self._mime

    def setText(self, text: str) -> None:
        mime = FakeMimeData()
        mime.setText(text)
        self._mime = mime

    def text(self) -> str:
        return self._mime.text()


class FakeApplication:
    _clipboard = FakeClipboard()

    @classmethod
    def clipboard(cls) -> FakeClipboard:
        return cls._clipboard

    @classmethod
    def reset_clipboard(cls) -> None:
        cls._clipboard = FakeClipboard()


class FakeQDialog:
    class DialogCode:
        Accepted = 1

    Accepted = 1

    def exec(self) -> int:
        return self.DialogCode.Accepted

    def exec_(self) -> int:
        return self.Accepted


class FakeQDialogButtonBox:
    class StandardButton:
        Ok = 1
        Cancel = 2

    Ok = 1
    Cancel = 2


class FakeQFontDialog:
    @staticmethod
    def getFont():
        return None, False


class FakeQFormLayout:
    def __init__(self, parent=None) -> None:
        self.parent = parent

    def addRow(self, *args, **kwargs) -> None:
        return None


class FakeQInputDialog:
    @staticmethod
    def getText(*args, **kwargs):
        return "", False


class FakeQLineEdit:
    class EchoMode:
        Normal = 0

    Normal = 0

    def __init__(self) -> None:
        self._text = ""

    def setPlaceholderText(self, _text: str) -> None:
        return None

    def text(self) -> str:
        return self._text


def load_addon_module(
    module_basename: str,
    *,
    mw: types.SimpleNamespace | None = None,
    aqt_overrides: dict | None = None,
    qt_overrides: dict | None = None,
    utils_overrides: dict | None = None,
    webview_overrides: dict | None = None,
    extra_modules: dict[str, types.ModuleType] | None = None,
):
    _install_fake_aqt(
        mw=mw if mw is not None else make_mw(),
        aqt_overrides=aqt_overrides,
        qt_overrides=qt_overrides,
        utils_overrides=utils_overrides,
        webview_overrides=webview_overrides,
        extra_modules=extra_modules,
    )

    package_name = f"text_tools_testpkg_{uuid.uuid4().hex}"
    package = types.ModuleType(package_name)
    package.__path__ = [str(ADDON_ROOT)]
    package.__file__ = str(ADDON_ROOT / "__init__.py")
    sys.modules[package_name] = package

    return _load_module(
        f"{package_name}.{module_basename}",
        ADDON_ROOT / f"{module_basename}.py",
    )


def make_fake_qt_for_actions() -> dict:
    return {
        "QApplication": FakeApplication,
        "QDialog": FakeQDialog,
        "QDialogButtonBox": FakeQDialogButtonBox,
        "QFontDialog": FakeQFontDialog,
        "QFormLayout": FakeQFormLayout,
        "QInputDialog": FakeQInputDialog,
        "QLineEdit": FakeQLineEdit,
        "QMimeData": FakeMimeData,
    }


def make_fake_qt_for_menu_builder() -> dict:
    return {
        "QAction": FakeAction,
        "QMenu": FakeMenu,
    }


def find_submenu(menu: FakeMenu, title: str) -> FakeMenu | None:
    for action in menu.actions():
        submenu = action.menu()
        if submenu and submenu.title() == title:
            return submenu
    return None


def visible_action_labels(menu: FakeMenu) -> list[str]:
    return [action.text() for action in menu.actions() if not action.is_separator]


def _install_fake_aqt(
    *,
    mw,
    aqt_overrides: dict | None = None,
    qt_overrides: dict | None = None,
    utils_overrides: dict | None = None,
    webview_overrides: dict | None = None,
    extra_modules: dict[str, types.ModuleType] | None = None,
) -> None:
    fake_aqt = types.ModuleType("aqt")
    fake_aqt.mw = mw
    for name, value in (aqt_overrides or {}).items():
        setattr(fake_aqt, name, value)

    fake_qt = types.ModuleType("aqt.qt")
    for name, value in (qt_overrides or {}).items():
        setattr(fake_qt, name, value)

    fake_utils = types.ModuleType("aqt.utils")
    fake_utils.showInfo = lambda *args, **kwargs: None
    for name, value in (utils_overrides or {}).items():
        setattr(fake_utils, name, value)

    fake_webview = types.ModuleType("aqt.webview")
    fake_webview.AnkiWebView = object
    for name, value in (webview_overrides or {}).items():
        setattr(fake_webview, name, value)

    fake_aqt.qt = fake_qt
    fake_aqt.utils = fake_utils
    fake_aqt.webview = fake_webview

    sys.modules["aqt"] = fake_aqt
    sys.modules["aqt.qt"] = fake_qt
    sys.modules["aqt.utils"] = fake_utils
    sys.modules["aqt.webview"] = fake_webview
    for module_name, module in (extra_modules or {}).items():
        sys.modules[module_name] = module


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
