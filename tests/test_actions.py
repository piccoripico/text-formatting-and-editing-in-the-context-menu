from __future__ import annotations

import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

from helpers import FakeApplication, load_addon_module, make_fake_qt_for_actions, make_mw


class FakeMedia:
    def __init__(self, *, return_value: str | None = None, error: Exception | None = None) -> None:
        self.return_value = return_value
        self.error = error
        self.calls: list[str] = []

    def add_file(self, path: str) -> str:
        self.calls.append(path)
        if self.error is not None:
            raise self.error
        if self.return_value is None:
            raise RuntimeError("No media filename configured")
        return self.return_value


class ActionsTests(unittest.TestCase):
    def setUp(self) -> None:
        FakeApplication.reset_clipboard()

    def _load_module(self, *, mw=None, show_info_messages: list[str] | None = None):
        utils_overrides = {}
        if show_info_messages is not None:
            utils_overrides["showInfo"] = show_info_messages.append

        return load_addon_module(
            "actions",
            mw=mw if mw is not None else make_mw(),
            qt_overrides=make_fake_qt_for_actions(),
            utils_overrides=utils_overrides,
        )

    def test_normalize_image_source_imports_existing_local_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            image_path = Path(tmp_dir) / "example.png"
            image_path.write_bytes(b"png")

            media = FakeMedia(return_value="example-imported.png")
            mw = make_mw()
            mw.col = types.SimpleNamespace(media=media)
            module = self._load_module(mw=mw)

            result = module._normalize_image_source(str(image_path))

        self.assertEqual(result, "example-imported.png")
        self.assertEqual(media.calls, [str(image_path.resolve())])

    def test_normalize_image_source_returns_empty_string_when_media_import_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            image_path = Path(tmp_dir) / "example.png"
            image_path.write_bytes(b"png")

            messages: list[str] = []
            media = FakeMedia(error=RuntimeError("boom"))
            mw = make_mw()
            mw.col = types.SimpleNamespace(media=media)
            module = self._load_module(mw=mw, show_info_messages=messages)

            result = module._normalize_image_source(str(image_path))

        self.assertEqual(result, "")
        self.assertEqual(len(messages), 1)
        self.assertIn(str(image_path), messages[0])
        self.assertIn("boom", messages[0])

    def test_set_clipboard_selection_preserves_html_when_present(self) -> None:
        module = self._load_module()

        copied = module._set_clipboard_selection({"html": "<b>Hello</b>", "text": "Hello"})

        self.assertTrue(copied)
        mime = module.QApplication.clipboard().mimeData()
        self.assertTrue(mime.hasHtml())
        self.assertEqual(mime.html(), "<b>Hello</b>")
        self.assertEqual(mime.text(), "Hello")

    def test_dispatch_spec_reviewer_cut_deletes_selection_after_copying_to_clipboard(self) -> None:
        module = self._load_module()
        calls: list[dict] = []

        def fake_run_js(_web, payload, callback=None) -> None:
            calls.append(payload)
            if callback is not None:
                callback({"html": "<b>Cut</b>", "text": "Cut"})

        spec = types.SimpleNamespace(action="cut", arg=None)

        with mock.patch.object(module, "_run_js", side_effect=fake_run_js):
            module.dispatch_spec(object(), spec, "reviewer")

        self.assertEqual(calls, [{"op": "getSelectedContent"}, {"op": "deleteSelection"}])
        mime = module.QApplication.clipboard().mimeData()
        self.assertEqual(mime.html(), "<b>Cut</b>")
        self.assertEqual(mime.text(), "Cut")

    def test_dispatch_user_word_routes_by_context(self) -> None:
        module = self._load_module()
        web = object()

        with (
            mock.patch.object(module, "_insert_text_editor_native") as insert_text,
            mock.patch.object(module, "_run_js") as run_js,
        ):
            module.dispatch_user_word(web, "Alpha", "editor")
            module.dispatch_user_word(web, "Beta", "reviewer")

        insert_text.assert_called_once_with(web, "Alpha")
        run_js.assert_called_once_with(web, {"op": "insertText", "text": "Beta"})


if __name__ == "__main__":
    unittest.main()
