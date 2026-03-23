from __future__ import annotations

import types
import unittest
from unittest import mock

from helpers import (
    FakeAction,
    FakeMenu,
    load_addon_module,
    make_fake_qt_for_actions,
    make_fake_qt_for_menu_builder,
    make_mw,
)


class FakeHookList(list):
    pass


class FakeGuiHooks:
    def __init__(self) -> None:
        self.editor_will_show_context_menu = FakeHookList()
        self.reviewer_will_show_context_menu = FakeHookList()
        self.webview_will_show_context_menu = FakeHookList()
        self.webview_will_set_content = FakeHookList()


class FakeEditor:
    pass


class FakeEditorWebView:
    pass


class FakeReviewer:
    def __init__(self, web=None) -> None:
        self.web = web


def _combined_fake_qt() -> dict:
    qt = make_fake_qt_for_actions()
    qt.update(make_fake_qt_for_menu_builder())
    return qt


class HooksTests(unittest.TestCase):
    def setUp(self) -> None:
        self.gui_hooks = FakeGuiHooks()
        self.editor_module = types.ModuleType("aqt.editor")
        self.editor_module.Editor = FakeEditor
        self.editor_module.EditorWebView = FakeEditorWebView

        self.reviewer_module = types.ModuleType("aqt.reviewer")
        self.reviewer_module.Reviewer = FakeReviewer

        self.mw = make_mw()
        self.mw.state = None
        self.mw.addonManager.addonFromModule = lambda _name: "test-addon"

        self.module = load_addon_module(
            "hooks",
            mw=self.mw,
            aqt_overrides={"gui_hooks": self.gui_hooks},
            qt_overrides=_combined_fake_qt(),
            extra_modules={
                "aqt.editor": self.editor_module,
                "aqt.reviewer": self.reviewer_module,
            },
        )

    def test_menu_has_text_tools_ignores_broken_actions(self) -> None:
        menu = FakeMenu("Root")
        broken_action = mock.Mock()
        broken_action.text.side_effect = RuntimeError("broken")
        menu.addAction(broken_action)
        menu.addAction(FakeAction("Text Tools", menu))

        self.assertTrue(self.module._menu_has_text_tools(menu))

    def test_on_editor_context_menu_builds_menu_only_when_enabled_and_missing(self) -> None:
        menu = FakeMenu("Root")
        webview = FakeEditorWebView()

        with (
            mock.patch.object(
                self.module, "load_config", return_value={"editor": {"enabled": True}}
            ),
            mock.patch.object(self.module, "build_context_menu") as build_context_menu,
        ):
            self.module._on_editor_context_menu(webview, menu)

        build_context_menu.assert_called_once_with(menu, "editor", webview)

        menu.addAction(FakeAction("Text Tools", menu))
        with (
            mock.patch.object(
                self.module, "load_config", return_value={"editor": {"enabled": True}}
            ),
            mock.patch.object(self.module, "build_context_menu") as build_context_menu,
        ):
            self.module._on_editor_context_menu(webview, menu)

        build_context_menu.assert_not_called()

        empty_menu = FakeMenu("Root")
        with (
            mock.patch.object(
                self.module, "load_config", return_value={"editor": {"enabled": False}}
            ),
            mock.patch.object(self.module, "build_context_menu") as build_context_menu,
        ):
            self.module._on_editor_context_menu(webview, empty_menu)

        build_context_menu.assert_not_called()

    def test_on_reviewer_context_menu_passes_reviewer_web(self) -> None:
        menu = FakeMenu("Root")
        reviewer_web = object()
        reviewer = FakeReviewer(web=reviewer_web)

        with (
            mock.patch.object(
                self.module, "load_config", return_value={"reviewer": {"enabled": True}}
            ),
            mock.patch.object(self.module, "build_context_menu") as build_context_menu,
        ):
            self.module._on_reviewer_context_menu(reviewer, menu)

        build_context_menu.assert_called_once_with(menu, "reviewer", reviewer_web)

    def test_on_webview_context_menu_only_runs_during_review(self) -> None:
        webview = object()
        menu = FakeMenu("Root")

        with (
            mock.patch.object(
                self.module, "load_config", return_value={"reviewer": {"enabled": True}}
            ),
            mock.patch.object(self.module, "build_context_menu") as build_context_menu,
        ):
            self.mw.state = "deckBrowser"
            self.module._on_webview_context_menu(webview, menu)
            self.mw.state = "review"
            self.module._on_webview_context_menu(webview, menu)

        build_context_menu.assert_called_once_with(menu, "reviewer", webview)

    def test_on_webview_context_menu_skips_disabled_or_existing_menu(self) -> None:
        webview = object()

        with (
            mock.patch.object(
                self.module, "load_config", return_value={"reviewer": {"enabled": False}}
            ),
            mock.patch.object(self.module, "build_context_menu") as build_context_menu,
        ):
            self.mw.state = "review"
            self.module._on_webview_context_menu(webview, FakeMenu("Root"))

        build_context_menu.assert_not_called()

        menu = FakeMenu("Root")
        menu.addAction(FakeAction("Text Tools", menu))
        with (
            mock.patch.object(
                self.module, "load_config", return_value={"reviewer": {"enabled": True}}
            ),
            mock.patch.object(self.module, "build_context_menu") as build_context_menu,
        ):
            self.mw.state = "review"
            self.module._on_webview_context_menu(webview, menu)

        build_context_menu.assert_not_called()

    def test_on_webview_will_set_content_injects_js_for_supported_contexts(self) -> None:
        web_content = types.SimpleNamespace(js=[])

        self.module._on_webview_will_set_content(web_content, FakeEditor())
        self.module._on_webview_will_set_content(web_content, FakeEditorWebView())
        self.module._on_webview_will_set_content(web_content, FakeReviewer())
        self.module._on_webview_will_set_content(web_content, object())

        self.assertEqual(
            web_content.js,
            [
                "/_addons/test-addon/web/commands.js",
                "/_addons/test-addon/web/commands.js",
                "/_addons/test-addon/web/commands.js",
            ],
        )

    def test_register_hooks_appends_all_handlers(self) -> None:
        self.module.register_hooks()

        self.assertEqual(
            self.gui_hooks.editor_will_show_context_menu,
            [self.module._on_editor_context_menu],
        )
        self.assertEqual(
            self.gui_hooks.reviewer_will_show_context_menu,
            [self.module._on_reviewer_context_menu],
        )
        self.assertEqual(
            self.gui_hooks.webview_will_show_context_menu,
            [self.module._on_webview_context_menu],
        )
        self.assertEqual(
            self.gui_hooks.webview_will_set_content,
            [self.module._on_webview_will_set_content],
        )


if __name__ == "__main__":
    unittest.main()
