# Text Tools in Right-Click Menu

An Anki add-on that adds a **Text Tools** menu to the editor **right-click menu**, providing quick access to common formatting, insertion, and editing commands.

- Available on AnkiWeb: https://ankiweb.net/shared/info/2143302836
- [GitHub repository](https://github.com/piccoripico/Text-Formatting-and-Editing-in-the-Context-Menu)
- [Japanese README (日本語)](https://github.com/piccoripico/Text-Formatting-and-Editing-in-the-Context-Menu/blob/main/docs/README_ja.md)

![Screenshot: editor right-click menu](https://raw.githubusercontent.com/piccoripico/Text-Formatting-and-Editing-in-the-Context-Menu/main/docs/Screenshot_right-click_menu.png)

## Features

- **Formatting:** bold, italic, underline, strikethrough, small text, superscript, subscript, monospace, inline code
- **Colors & size:** text color, highlight color, font size presets, font selection dialog
- **Layout:** text alignment, indent/outdent, ordered/unordered lists
- **Insert:** links, images, ruby text, tables, date/time, math snippets, blockquotes, horizontal rules, special characters
  Local image files are imported into Anki's media collection before insertion.
- **Edit:** cut, copy, paste, paste as plain text, remove link, select all, undo/redo, clear all formatting
- **Extras:** style presets, word count

### Optional

#### Quick Items

- Select frequently used commands for quicker access.
- By default, they are shown near the top of the **Text Tools** menu.
- They can also be displayed at the top level of the right-click menu.

#### User Words

- Register your own words or short snippets and insert them from the **User Words** submenu.
- They can also be displayed at the top level of the right-click menu.

## Reviewer support

The add-on can also display **Text Tools** in the reviewer right-click menu. Most reviewer-side features are available when [**Edit Field During Review (Cloze)**](https://ankiweb.net/shared/info/385888438) is installed.

Reviewer support was the original motivation behind the development of this add-on.

## Config

Open:

> Tools → Add-ons → Text Tools in Right-Click Menu → Config

The configuration window has three tabs:

- **General** — show **Text Tools** in the editor and/or reviewer right-click menu
- **Quick Items** — choose frequently used items and optionally display them at the top level of the right-click menu
- **User Words** — add, edit, remove, reorder, import, or export your own words and optionally display them at the top level of the right-click menu

![Screenshot: config window](https://raw.githubusercontent.com/piccoripico/Text-Formatting-and-Editing-in-the-Context-Menu/main/docs/Screenshot_config.png)

## Build

Create a clean `.ankiaddon` package with:

```bash
py -3 scripts/build_ankiaddon.py
```

This writes `dist/Text-Tools.ankiaddon` and packages the contents of `Text-Tools/` at the archive root.

The build intentionally excludes generated files such as:

- `__pycache__/`
- `*.pyc`
- user-specific files inside `Text-Tools/user_files/` except `README.txt`

## Changelog

- 2026-03-08
  - Full rewrite of the add-on
  - Renamed the add-on from **Text Formatting and Editing in the Context Menu** to **Text Tools in Right-Click Menu**
  - Added style presets, ruby insertion, table insertion, and other enhancements
- 2025-04-15
  - Fixed an issue that prevented the configuration window from opening
- 2023-09-03
  - Added a note about the reviewer context menu to the configuration window (thanks for the feedback)
- 2023-08-16
  - Added the User Words feature
- 2023-07-29
  - Added an option to display Quick Items at the top level of the context menu
- 2023-07-27
  - Added a configuration window (please restart Anki after updating the add-on)
  - Added the Quick Items feature
  - Fixed several bugs
