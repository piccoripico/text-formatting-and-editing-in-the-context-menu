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


class FakeFont:
    def __init__(
        self,
        *,
        family: str = "Serif",
        point_size: int = 0,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        strike_out: bool = False,
    ) -> None:
        self._family = family
        self._point_size = point_size
        self._bold = bold
        self._italic = italic
        self._underline = underline
        self._strike_out = strike_out

    def family(self) -> str:
        return self._family

    def pointSize(self) -> int:
        return self._point_size

    def bold(self) -> bool:
        return self._bold

    def italic(self) -> bool:
        return self._italic

    def underline(self) -> bool:
        return self._underline

    def strikeOut(self) -> bool:
        return self._strike_out


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

    def test_normalize_image_source_leaves_remote_urls_unchanged(self) -> None:
        module = self._load_module()

        result = module._normalize_image_source("https://example.com/image.png")

        self.assertEqual(result, "https://example.com/image.png")

    def test_normalize_image_source_imports_file_uris(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            image_path = Path(tmp_dir) / "example.png"
            image_path.write_bytes(b"png")

            media = FakeMedia(return_value="from-file-uri.png")
            mw = make_mw()
            mw.col = types.SimpleNamespace(media=media)
            module = self._load_module(mw=mw)

            result = module._normalize_image_source(image_path.resolve().as_uri())

        self.assertEqual(result, "from-file-uri.png")
        self.assertEqual(media.calls, [str(image_path.resolve())])

    def test_set_clipboard_selection_preserves_html_when_present(self) -> None:
        module = self._load_module()

        copied = module._set_clipboard_selection({"html": "<b>Hello</b>", "text": "Hello"})

        self.assertTrue(copied)
        mime = module.QApplication.clipboard().mimeData()
        self.assertTrue(mime.hasHtml())
        self.assertEqual(mime.html(), "<b>Hello</b>")
        self.assertEqual(mime.text(), "Hello")

    def test_set_clipboard_selection_returns_false_for_empty_content(self) -> None:
        module = self._load_module()

        copied = module._set_clipboard_selection({"html": "", "text": ""})

        self.assertFalse(copied)

    def test_paste_from_clipboard_editor_native_prefers_html(self) -> None:
        module = self._load_module()
        mime = module.QMimeData()
        mime.setHtml("<b>Hello</b>")
        mime.setText("Hello")
        module.QApplication.clipboard().setMimeData(mime)

        with (
            mock.patch.object(module, "_insert_html_editor_native") as insert_html,
            mock.patch.object(module, "_insert_text_editor_native") as insert_text,
        ):
            module._paste_from_clipboard_editor_native(object())

        insert_html.assert_called_once_with(mock.ANY, "<b>Hello</b>")
        insert_text.assert_not_called()

    def test_paste_from_clipboard_editor_native_falls_back_to_plain_text(self) -> None:
        module = self._load_module()
        module.QApplication.clipboard().setText("Hello")

        with (
            mock.patch.object(module, "_insert_html_editor_native") as insert_html,
            mock.patch.object(module, "_insert_text_editor_native") as insert_text,
        ):
            module._paste_from_clipboard_editor_native(object())

        insert_html.assert_not_called()
        insert_text.assert_called_once_with(mock.ANY, "Hello")

    def test_paste_from_clipboard_reviewer_prefers_html(self) -> None:
        module = self._load_module()
        mime = module.QMimeData()
        mime.setHtml("<i>Hello</i>")
        mime.setText("Hello")
        module.QApplication.clipboard().setMimeData(mime)

        with mock.patch.object(module, "_run_js") as run_js:
            module._paste_from_clipboard_reviewer(object())

        run_js.assert_called_once_with(mock.ANY, {"op": "insertHTML", "html": "<i>Hello</i>"})

    def test_paste_from_clipboard_reviewer_falls_back_to_plain_text(self) -> None:
        module = self._load_module()
        module.QApplication.clipboard().setText("Hello")

        with mock.patch.object(module, "_run_js") as run_js:
            module._paste_from_clipboard_reviewer(object())

        run_js.assert_called_once_with(mock.ANY, {"op": "insertText", "text": "Hello"})

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

    def test_dispatch_spec_editor_insert_image_prompt_escapes_inserted_src(self) -> None:
        module = self._load_module()
        web = object()
        spec = types.SimpleNamespace(action="insert_image_prompt", arg=None)

        with (
            mock.patch.object(module.QInputDialog, "getText", return_value=("ignored", True)),
            mock.patch.object(module, "_normalize_image_source", return_value='image"name.png'),
            mock.patch.object(module, "_insert_html_editor_native") as insert_html,
        ):
            module.dispatch_spec(web, spec, "editor")

        insert_html.assert_called_once_with(web, '<img src="image&quot;name.png">')

    def test_dispatch_spec_reviewer_insert_image_prompt_uses_js_insert_image(self) -> None:
        module = self._load_module()
        web = object()
        spec = types.SimpleNamespace(action="insert_image_prompt", arg=None)

        with (
            mock.patch.object(module.QInputDialog, "getText", return_value=("ignored", True)),
            mock.patch.object(module, "_normalize_image_source", return_value="image.png"),
            mock.patch.object(module, "_run_js") as run_js,
        ):
            module.dispatch_spec(web, spec, "reviewer")

        run_js.assert_called_once_with(web, {"op": "insertImage", "url": "image.png"})

    def test_dispatch_spec_editor_font_dialog_applies_editor_commands(self) -> None:
        module = self._load_module()
        web = object()
        font = FakeFont(
            family="Noto Serif",
            point_size=16,
            bold=True,
            italic=True,
            underline=True,
            strike_out=True,
        )
        spec = types.SimpleNamespace(action="font_dialog", arg=None)

        with (
            mock.patch.object(module.QFontDialog, "getFont", return_value=(font, True)),
            mock.patch.object(module, "_editor_set_format") as editor_set_format,
        ):
            module.dispatch_spec(web, spec, "editor")

        self.assertEqual(
            editor_set_format.call_args_list,
            [
                mock.call(web, "fontname", "Noto Serif"),
                mock.call(web, "fontsize", 5),
                mock.call(web, "bold"),
                mock.call(web, "italic"),
                mock.call(web, "underline"),
                mock.call(web, "strikethrough"),
            ],
        )

    def test_dispatch_spec_reviewer_font_dialog_builds_css_style_payload(self) -> None:
        module = self._load_module()
        web = object()
        font = FakeFont(
            family="Noto Sans",
            point_size=13,
            bold=True,
            italic=True,
            underline=True,
            strike_out=True,
        )
        spec = types.SimpleNamespace(action="font_dialog", arg=None)

        with (
            mock.patch.object(module.QFontDialog, "getFont", return_value=(font, True)),
            mock.patch.object(module, "_run_js") as run_js,
        ):
            module.dispatch_spec(web, spec, "reviewer")

        run_js.assert_called_once_with(
            web,
            {
                "op": "applyStyle",
                "style": {
                    "fontFamily": "Noto Sans",
                    "fontSize": "13pt",
                    "fontWeight": "bold",
                    "fontStyle": "italic",
                    "textDecoration": "underline line-through",
                },
            },
        )

    def test_dispatch_spec_word_count_formats_show_info_message(self) -> None:
        messages: list[str] = []
        module = self._load_module(show_info_messages=messages)
        web = object()
        spec = types.SimpleNamespace(action="word_count", arg=None)

        def fake_run_js(_web, payload, callback=None) -> None:
            self.assertEqual(payload, {"op": "wordCount"})
            if callback is not None:
                callback({"words": 3, "characters": 10})

        with mock.patch.object(module, "_run_js", side_effect=fake_run_js):
            module.dispatch_spec(web, spec, "reviewer")

        self.assertEqual(messages, ["Words: 3\nCharacters: 10"])

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
