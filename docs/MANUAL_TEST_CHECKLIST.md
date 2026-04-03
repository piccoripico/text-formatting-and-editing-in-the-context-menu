# Manual Test Checklist

Use this checklist before uploading a new `.ankiaddon` release to AnkiWeb.

## Setup

1. Build a fresh package with `py -3 scripts/build_ankiaddon.py`.
2. Install the generated `dist/Text-Tools.ankiaddon` into a test Anki profile.
3. Restart Anki after installation.
4. Open one note in the editor and one card in review mode.

## Editor Menu

1. Right-click inside an editor field.
2. Confirm `Text Tools` appears exactly once.
3. Open `Text Tools` and verify the expected top-level groups are present:
   `Style Presets`, `Text Styling`, `Text Color`, `Font Size`, `Alignment / List`, `Insert`, `Edit`.
4. Toggle a few representative commands and confirm they change the selected text:
   `Bold`, `Highlight Yellow`, `Justify Center`, `Clear All Formatting`.

## Quick Items And User Words

1. Open the add-on config screen from Anki's add-on list.
2. Enable a few Quick Items and choose whether they appear at the top level.
3. Add a few User Words and test both positions:
   top level and `Text Tools > User Words`.
4. Re-open the context menu and confirm the layout matches the saved config.

## Clipboard And Insert Actions

1. Copy formatted text inside the editor and paste it back.
2. Confirm HTML formatting is preserved on normal paste.
3. Use `Paste Plain Text` and confirm formatting is removed.
4. Try `Insert Link`, `Insert Image`, `Insert Ruby`, `Horizontal Line`, and one table command.
5. For `Insert Image`, test both:
   a remote URL and a local file path.
6. After inserting a local image, confirm the image is stored in Anki's media collection and still works after restarting Anki.

## Reviewer Behavior

1. If `Edit Field During Review (Cloze)` is installed, enter review mode and open the reviewer context menu.
2. Confirm `Text Tools` appears only once in review mode.
3. Test representative reviewer actions:
   `Insert Text`, `Paste`, `Paste Plain Text`, `Copy`, `Cut`, `Clear All Formatting`, `Word Count`.
4. Confirm the menu does not appear on unrelated webviews outside review mode.

## Config Import And Export

1. Open the `User Words` tab in the config dialog.
2. Export the current list to `.txt`.
3. Clear the list and import the `.txt` file.
4. Confirm order and values round-trip as expected, including words containing commas.

## Release Sanity Check

1. Re-run:
   `py -3 -m ruff check .`
2. Re-run:
   `py -3 -m unittest discover -s tests -v`
3. Rebuild:
   `py -3 scripts/build_ankiaddon.py`
4. Confirm `dist/Text-Tools.ankiaddon` is the file you plan to upload.
