from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from helpers import load_addon_module, make_mw


class DummyDialog:
    class DialogCode:
        Accepted = 1

    Accepted = 1

    def __init__(self, *args, **kwargs) -> None:
        pass

    def exec(self) -> int:
        return self.DialogCode.Accepted

    def exec_(self) -> int:
        return self.Accepted


class DummyDialogButtonBox:
    class StandardButton:
        Ok = 1
        Cancel = 2

    Ok = 1
    Cancel = 2


class DummyLineEdit:
    class EchoMode:
        Normal = 0

    Normal = 0


class DummySizePolicy:
    class Policy:
        Maximum = 1
        Fixed = 2

    Maximum = 1
    Fixed = 2


class DummyQt:
    class ScrollBarPolicy:
        ScrollBarAsNeeded = 1
        ScrollBarAlwaysOff = 2

    class AlignmentFlag:
        AlignLeft = 1
        AlignTop = 2

    ScrollBarAsNeeded = 1
    ScrollBarAlwaysOff = 2
    AlignLeft = 1
    AlignTop = 2


class DummyFileDialog:
    @staticmethod
    def getOpenFileName(*args, **kwargs):
        return "", ""

    @staticmethod
    def getSaveFileName(*args, **kwargs):
        return "", ""


class DummyWidget:
    def __init__(self, *args, **kwargs) -> None:
        pass


class FakeCheckBox:
    def __init__(self, text: str, checked: bool = False) -> None:
        self._text = text
        self._checked = checked

    def text(self) -> str:
        return self._text

    def isChecked(self) -> bool:
        return self._checked

    def setChecked(self, checked: bool) -> None:
        self._checked = checked


class FakeListItem:
    def __init__(self, text: str) -> None:
        self._text = text

    def text(self) -> str:
        return self._text

    def setText(self, text: str) -> None:
        self._text = text


class FakeListWidget:
    def __init__(self, items: list[str] | None = None, current_row: int = -1) -> None:
        self._items = [FakeListItem(item) for item in (items or [])]
        self._current_row = current_row

    def addItem(self, value) -> None:
        item = value if isinstance(value, FakeListItem) else FakeListItem(str(value))
        self._items.append(item)

    def addItems(self, values: list[str]) -> None:
        for value in values:
            self.addItem(value)

    def clear(self) -> None:
        self._items = []
        self._current_row = -1

    def count(self) -> int:
        return len(self._items)

    def currentItem(self) -> FakeListItem | None:
        if 0 <= self._current_row < len(self._items):
            return self._items[self._current_row]
        return None

    def currentRow(self) -> int:
        return self._current_row

    def insertItem(self, row: int, item) -> None:
        value = item if isinstance(item, FakeListItem) else FakeListItem(str(item))
        self._items.insert(row, value)

    def item(self, row: int) -> FakeListItem:
        return self._items[row]

    def row(self, item: FakeListItem) -> int:
        return self._items.index(item)

    def setCurrentRow(self, row: int) -> None:
        self._current_row = row

    def takeItem(self, row: int) -> FakeListItem:
        item = self._items.pop(row)
        if self._current_row >= len(self._items):
            self._current_row = len(self._items) - 1
        return item

    def texts(self) -> list[str]:
        return [item.text() for item in self._items]


def _fake_qt_for_config_dialog() -> dict:
    return {
        "QCheckBox": DummyWidget,
        "QDialog": DummyDialog,
        "QDialogButtonBox": DummyDialogButtonBox,
        "QFileDialog": DummyFileDialog,
        "QGroupBox": DummyWidget,
        "QHBoxLayout": DummyWidget,
        "QInputDialog": DummyWidget,
        "QLabel": DummyWidget,
        "QLineEdit": DummyLineEdit,
        "QListWidget": DummyWidget,
        "QPushButton": DummyWidget,
        "QScrollArea": DummyWidget,
        "QSizePolicy": DummySizePolicy,
        "Qt": DummyQt,
        "QTabWidget": DummyWidget,
        "QVBoxLayout": DummyWidget,
        "QWidget": DummyWidget,
    }


class ConfigDialogTests(unittest.TestCase):
    def _load_module(self, *, config=None, mw=None):
        if mw is None:
            mw = make_mw(config)
        return load_addon_module("config_dialog", mw=mw, qt_overrides=_fake_qt_for_config_dialog())

    def _make_dialog(self, module):
        dialog = module.ConfigDialog.__new__(module.ConfigDialog)
        dialog.config = {
            "editor": {"enabled": True},
            "reviewer": {"enabled": True},
            "selected_quick_access_items": [],
            "quick_access_position": False,
            "user_words_flag": True,
            "user_words": [],
            "user_words_position": False,
        }
        dialog.quick_access_checkboxes = []
        dialog.words_list_widget = FakeListWidget()
        dialog.editor_checkbox = FakeCheckBox("editor", True)
        dialog.reviewer_checkbox = FakeCheckBox("reviewer", True)
        dialog.quick_access_position_checkbox = FakeCheckBox("quick_access", False)
        dialog.words_checkbox = FakeCheckBox("words", True)
        dialog.words_position_checkbox = FakeCheckBox("words_position", False)
        dialog.accept = mock.Mock()
        return dialog

    def test_register_config_action_registers_open_handler(self) -> None:
        mw = make_mw()
        mw.addonManager.setConfigAction = mock.Mock()
        module = self._load_module(mw=mw)

        module.register_config_action()

        mw.addonManager.setConfigAction.assert_called_once_with(
            module.ADDON_MODULE,
            module.open_config_dialog,
        )

    def test_move_up_and_down_reorder_user_words(self) -> None:
        module = self._load_module()
        dialog = self._make_dialog(module)
        dialog.words_list_widget = FakeListWidget(["Alpha", "Beta", "Gamma"], current_row=1)

        dialog._move_up()
        self.assertEqual(dialog.words_list_widget.texts(), ["Beta", "Alpha", "Gamma"])
        self.assertEqual(dialog.words_list_widget.currentRow(), 0)

        dialog.words_list_widget.setCurrentRow(1)
        dialog._move_down()
        self.assertEqual(dialog.words_list_widget.texts(), ["Beta", "Gamma", "Alpha"])
        self.assertEqual(dialog.words_list_widget.currentRow(), 2)

    def test_import_words_reads_text_files(self) -> None:
        module = self._load_module()
        dialog = self._make_dialog(module)

        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "words.txt"
            path.write_text(" Alpha \n\nBeta\nGamma\n", encoding="utf-8")

            with mock.patch.object(
                module.QFileDialog, "getOpenFileName", return_value=(str(path), "")
            ):
                dialog._import_words()

        self.assertEqual(dialog.words_list_widget.texts(), ["Alpha", "Beta", "Gamma"])

    def test_export_words_writes_text_file(self) -> None:
        module = self._load_module()
        dialog = self._make_dialog(module)
        dialog.words_list_widget = FakeListWidget(["Alpha", "Beta,Gamma"])

        with tempfile.TemporaryDirectory() as tmp_dir:
            text_path = Path(tmp_dir) / "words.txt"

            with mock.patch.object(
                module.QFileDialog, "getSaveFileName", return_value=(str(text_path), "")
            ):
                dialog._export_words()

            self.assertEqual(text_path.read_text(encoding="utf-8"), "Alpha\nBeta,Gamma\n")

    def test_export_words_adds_txt_extension_when_missing(self) -> None:
        module = self._load_module()
        dialog = self._make_dialog(module)
        dialog.words_list_widget = FakeListWidget(["Alpha", "Beta"])

        with tempfile.TemporaryDirectory() as tmp_dir:
            path_without_suffix = Path(tmp_dir) / "user_words"

            with mock.patch.object(
                module.QFileDialog,
                "getSaveFileName",
                return_value=(str(path_without_suffix), ""),
            ):
                dialog._export_words()

            exported_path = path_without_suffix.with_suffix(".txt")
            self.assertTrue(exported_path.exists())
            self.assertEqual(exported_path.read_text(encoding="utf-8"), "Alpha\nBeta\n")

    def test_save_and_close_updates_config_and_persists_it(self) -> None:
        module = self._load_module()
        dialog = self._make_dialog(module)
        dialog.quick_access_checkboxes = [
            FakeCheckBox("Bold", True),
            FakeCheckBox("Italic", False),
            FakeCheckBox("Highlight Red", True),
        ]
        dialog.words_list_widget = FakeListWidget(["Alpha", "Beta"])
        dialog.editor_checkbox.setChecked(False)
        dialog.reviewer_checkbox.setChecked(True)
        dialog.quick_access_position_checkbox.setChecked(True)
        dialog.words_checkbox.setChecked(False)
        dialog.words_position_checkbox.setChecked(True)

        with mock.patch.object(module, "save_config") as save_config:
            dialog._save_and_close()

        self.assertEqual(
            dialog.config,
            {
                "editor": {"enabled": False},
                "reviewer": {"enabled": True},
                "selected_quick_access_items": ["Bold", "Highlight Red"],
                "quick_access_position": True,
                "user_words_flag": False,
                "user_words": ["Alpha", "Beta"],
                "user_words_position": True,
            },
        )
        save_config.assert_called_once_with(dialog.config)
        dialog.accept.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
