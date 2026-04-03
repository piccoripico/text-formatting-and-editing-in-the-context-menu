# Text Tools in Right-Click Menu

An Anki add-on that adds a **Text Tools** menu to the editor **right-click menu**, making common formatting, insertion, and editing commands much easier to reach.

- AnkiWeb: https://ankiweb.net/shared/info/2143302836
- [Japanese README](docs/README_ja.md)

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
- `tests/`: automated checks for config migration, menu definitions, action dispatch, menu building, and packaging
- `tests-js/`: DOM-level automated checks for reviewer-side web commands

## Development

Install Ruff if needed:

```bash
py -3 -m pip install ruff
npm.cmd install
```

Run lint and formatting:

```bash
py -3 -m ruff check .
py -3 -m ruff format .
```

Run tests:

```bash
py -3 -m unittest discover -s tests -v
npm.cmd run test:js
```

Build a clean `.ankiaddon` package:

```bash
py -3 scripts/build_ankiaddon.py
```

This writes `dist/Text-Tools.ankiaddon` and packages the contents of `Text-Tools/` at the archive root while excluding generated files such as `__pycache__/`, `*.pyc`, and user-specific files inside `Text-Tools/user_files/` except `README.txt`.

## Release Flow

1. Run the lint and format commands above.
2. Run through the manual smoke test checklist in `docs/MANUAL_TEST_CHECKLIST.md`.
3. Build `dist/Text-Tools.ankiaddon`.
4. Push a version tag such as `v2.1.0` to create a GitHub release automatically.
5. Upload the generated `.ankiaddon` file to AnkiWeb manually.

The GitHub Actions workflow at `.github/workflows/release.yml` runs Ruff, Python tests, DOM tests, builds `dist/Text-Tools.ankiaddon`, and attaches that file to the GitHub release for the pushed tag.
