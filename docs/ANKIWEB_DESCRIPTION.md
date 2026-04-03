# Text Tools in Right-Click Menu

Add a **Text Tools** menu to the editor **right-click menu** so common formatting, insertion, and editing commands are always close at hand.

![Screenshot: editor right-click menu](https://raw.githubusercontent.com/piccoripico/text-formatting-and-editing-in-the-context-menu/main/docs/Screenshot_right-click_menu.png)

## Features

- **Formatting:** bold, italic, underline, strikethrough, small text, superscript, subscript, monospace, inline code
- **Colors & size:** text color, highlight color, font size presets, font selection dialog
- **Layout:** text alignment, indent/outdent, ordered and unordered lists
- **Insert:** links, images, ruby text, tables, date/time, math snippets, blockquotes, horizontal rules, and special characters
- **Edit:** cut, copy, paste, paste as plain text, remove link, select all, undo/redo, clear all formatting
- **Extras:** style presets and word count

Local image files are imported into Anki's media collection before insertion.

## Optional features

### Quick Items

- Choose frequently used commands for quicker access.
- Show them near the top of the **Text Tools** menu or directly at the top level of the right-click menu.

### User Words

- Register your own words or short snippets and insert them from the **User Words** submenu.
- Show them inside **Text Tools** or directly at the top level of the right-click menu.

## Reviewer support

The add-on can also show **Text Tools** in the reviewer right-click menu. Most reviewer-side features are available when [**Edit Field During Review (Cloze)**](https://ankiweb.net/shared/info/385888438) is installed.

## Config

Open:

> Tools -> Add-ons -> Text Tools in Right-Click Menu -> Config

The configuration window has three tabs:

- **General**: show **Text Tools** in the editor and/or reviewer right-click menu
- **Quick Items**: choose frequently used items and optionally display them at the top level of the right-click menu
- **User Words**: add, edit, remove, reorder, import, or export your own words as plain text and optionally display them at the top level of the right-click menu

![Screenshot: config window](https://raw.githubusercontent.com/piccoripico/text-formatting-and-editing-in-the-context-menu/main/docs/Screenshot_config.png)

## Changelog

- 2026-04-04
  - Improved local image insertion by importing local files into Anki's media collection before insertion
  - Improved cut, copy, and paste behavior
- 2026-03-08
  - **Rewrote** the add-on **from the ground up**
  - Renamed the add-on from **Text Formatting and Editing in the Context Menu** to **Text Tools in Right-Click Menu**
  - Added style presets, ruby insertion, table insertion, and other improvements
- 2025-04-15
  - Fixed an issue that prevented the configuration window from opening
- 2023-09-03
  - Added a note about the reviewer context menu to the configuration window
- 2023-08-16
  - Added the User Words feature
- 2023-07-29
  - Added an option to display Quick Items at the top level of the right-click menu
- 2023-07-27
  - Added a configuration window
  - Added the Quick Items feature
  - Fixed several bugs
