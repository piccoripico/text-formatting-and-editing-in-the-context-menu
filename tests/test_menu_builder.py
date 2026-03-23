from __future__ import annotations

import unittest
from unittest import mock

from helpers import (
    find_submenu,
    load_addon_module,
    make_fake_qt_for_actions,
    make_fake_qt_for_menu_builder,
    visible_action_labels,
)


def _combined_fake_qt() -> dict:
    qt = make_fake_qt_for_actions()
    qt.update(make_fake_qt_for_menu_builder())
    return qt


def _action_by_label(menu, label: str):
    for action in menu.actions():
        if not action.is_separator and action.text() == label:
            return action
    raise AssertionError(f"Could not find action with label {label!r}")


class MenuBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_addon_module("menu_builder", qt_overrides=_combined_fake_qt())
        self.web = object()

    def test_build_context_menu_places_pinned_items_on_first_level(self) -> None:
        config = {
            "selected_quick_access_items": ["Bold", "Highlight Red", "Bold", "Missing"],
            "quick_access_position": True,
            "user_words_flag": True,
            "user_words": ["Alpha", "Beta"],
            "user_words_position": True,
        }

        with mock.patch.object(self.module, "load_config", return_value=config):
            parent_menu = self.module.QMenu("Root")
            self.module.build_context_menu(parent_menu, "editor", self.web)

        self.assertEqual(
            visible_action_labels(parent_menu),
            ["Bold", "Highlight Red", "Alpha", "Beta", "Text Tools"],
        )

        root_menu = find_submenu(parent_menu, "Text Tools")
        self.assertIsNotNone(root_menu)
        self.assertNotIn("Bold", visible_action_labels(root_menu))
        self.assertIsNone(find_submenu(root_menu, "User Words"))

    def test_build_context_menu_keeps_unpinned_items_inside_text_tools(self) -> None:
        config = {
            "selected_quick_access_items": ["Bold", "Highlight Red"],
            "quick_access_position": False,
            "user_words_flag": True,
            "user_words": ["Alpha", "Beta"],
            "user_words_position": False,
        }

        with mock.patch.object(self.module, "load_config", return_value=config):
            parent_menu = self.module.QMenu("Root")
            self.module.build_context_menu(parent_menu, "editor", self.web)

        self.assertEqual(visible_action_labels(parent_menu), ["Text Tools"])

        root_menu = find_submenu(parent_menu, "Text Tools")
        self.assertIsNotNone(root_menu)
        self.assertEqual(
            visible_action_labels(root_menu)[:4],
            ["Bold", "Highlight Red", "User Words", "Style Presets"],
        )

        user_words_menu = find_submenu(root_menu, "User Words")
        self.assertIsNotNone(user_words_menu)
        self.assertEqual(visible_action_labels(user_words_menu), ["Alpha", "Beta"])

    def test_action_callbacks_dispatch_selected_command_and_user_word(self) -> None:
        config = {
            "selected_quick_access_items": ["Bold"],
            "quick_access_position": True,
            "user_words_flag": True,
            "user_words": ["Alpha"],
            "user_words_position": True,
        }

        with (
            mock.patch.object(self.module, "load_config", return_value=config),
            mock.patch.object(self.module, "dispatch_spec") as dispatch_spec,
            mock.patch.object(self.module, "dispatch_user_word") as dispatch_user_word,
        ):
            parent_menu = self.module.QMenu("Root")
            self.module.build_context_menu(parent_menu, "editor", self.web)

            _action_by_label(parent_menu, "Bold").triggered.emit()
            _action_by_label(parent_menu, "Alpha").triggered.emit()

        dispatch_spec.assert_called_once()
        web_arg, spec_arg, context_arg = dispatch_spec.call_args.args
        self.assertIs(web_arg, self.web)
        self.assertEqual(spec_arg.label, "Bold")
        self.assertEqual(context_arg, "editor")
        dispatch_user_word.assert_called_once_with(self.web, "Alpha", "editor")


if __name__ == "__main__":
    unittest.main()
