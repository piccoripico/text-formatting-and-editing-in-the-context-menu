# Text Tools in Right-Click Menu

An Anki add-on that adds a **Text Tools** menu to the editor **right-click menu**, making common formatting, insertion, and editing commands much easier to reach.

- AnkiWeb: https://ankiweb.net/shared/info/2143302836
- [Japanese README](docs/README_ja.md)
- [AnkiWeb description draft](docs/ANKIWEB_DESCRIPTION.md)
- [AnkiWeb description draft (Japanese)](docs/ANKIWEB_DESCRIPTION_ja.md)

![Screenshot: editor right-click menu](docs/Screenshot_right-click_menu.png)

## Highlights

- Text styling, colors, font sizes, alignment, lists, and clear-format helpers
- Insert helpers for links, images, ruby text, tables, date/time, math snippets, blockquotes, and special characters
- Quick Items and User Words for faster access to frequently used actions
- Reviewer-side support, with broader functionality when [Edit Field During Review (Cloze)](https://ankiweb.net/shared/info/385888438) is installed

## Repository Layout

- `Text-Tools/`: the shipped Anki add-on package
- `docs/`: screenshots plus GitHub and AnkiWeb-facing documentation
- `scripts/`: release helpers such as `.ankiaddon` packaging
- `tests/`: automated checks for config migration, menu definitions, and packaging

The runtime code intentionally stays in `Text-Tools/` instead of moving to a generic `src/` directory. The release archive needs the add-on files at the archive root, so keeping the package layout close to the shipped structure reduces packaging complexity.

## Development

Install Ruff if needed:

```bash
py -3 -m pip install ruff
```

Run lint and formatting:

```bash
py -3 -m ruff check .
py -3 -m ruff format .
```

Run tests:

```bash
py -3 -m unittest discover -s tests -v
```

Build a clean `.ankiaddon` package:

```bash
py -3 scripts/build_ankiaddon.py
```

This writes `dist/Text-Tools.ankiaddon` and packages the contents of `Text-Tools/` at the archive root while excluding generated files such as `__pycache__/`, `*.pyc`, and user-specific files inside `Text-Tools/user_files/` except `README.txt`.

## Release Flow

1. Run the lint and format commands above.
2. Build `dist/Text-Tools.ankiaddon`.
3. Upload the generated `.ankiaddon` file to AnkiWeb manually.
