from __future__ import annotations

from aqt.qt import QAction, QMenu
from aqt.webview import AnkiWebView

from .actions import dispatch_spec, dispatch_user_word
from .config_store import load_config
from .menu_spec import COMMANDS, STYLE_PRESET_SECTIONS, CommandSpec


def _add_action(menu: QMenu, label: str, callback) -> None:
    action = QAction(label, menu)
    action.triggered.connect(callback)
    menu.addAction(action)


def _specs_for_context(context_name: str) -> list[CommandSpec]:
    return [spec for spec in COMMANDS if context_name in spec.contexts]


def _spec_by_label_for_context(context_name: str, label: str) -> CommandSpec | None:
    for spec in COMMANDS:
        if spec.label == label and context_name in spec.contexts:
            return spec
    return None


def _add_spec_action(menu: QMenu, web: AnkiWebView, spec: CommandSpec, context_name: str) -> None:
    _add_action(
        menu,
        spec.label,
        lambda _checked=False, s=spec, ctx=context_name: dispatch_spec(web, s, ctx),
    )


def _submenu_specs(
    context_name: str, category: str, submenu_path: tuple[str, ...] = ()
) -> list[CommandSpec]:
    specs = _specs_for_context(context_name)
    return [
        spec for spec in specs if spec.category == category and spec.submenu_path == submenu_path
    ]


def _category_specs(context_name: str, category: str) -> list[CommandSpec]:
    specs = _specs_for_context(context_name)
    return [spec for spec in specs if spec.category == category]


def _quick_access_specs(config: dict, context_name: str) -> list[CommandSpec]:
    specs: list[CommandSpec] = []
    seen_labels: set[str] = set()
    for label in config.get("selected_quick_access_items", []):
        spec = _spec_by_label_for_context(context_name, label)
        if spec and spec.quick_access_allowed and spec.label not in seen_labels:
            specs.append(spec)
            seen_labels.add(spec.label)
    return specs


def _get_or_create_submenu(parent: QMenu, title: str) -> QMenu:
    for action in parent.actions():
        submenu = action.menu()
        if submenu and submenu.title() == title:
            return submenu
    return parent.addMenu(title)


def _add_spec_into_menu_tree(
    parent: QMenu, spec: CommandSpec, web: AnkiWebView, context_name: str
) -> None:
    current_menu = parent
    for title in spec.submenu_path:
        current_menu = _get_or_create_submenu(current_menu, title)
    _add_spec_action(current_menu, web, spec, context_name)


def _add_user_words_first_level(
    config: dict, parent_menu: QMenu, web: AnkiWebView, context_name: str
) -> bool:
    if not config.get("user_words_flag", False):
        return False

    user_words = config.get("user_words", [])
    if not user_words:
        return False

    if not config.get("user_words_position", False):
        return False

    for word in user_words:
        _add_action(
            parent_menu,
            word,
            lambda _checked=False, w=word, ctx=context_name: dispatch_user_word(web, w, ctx),
        )
    return True


def _add_user_words_submenu(
    config: dict, root_menu: QMenu, web: AnkiWebView, context_name: str
) -> bool:
    if not config.get("user_words_flag", False):
        return False

    user_words = config.get("user_words", [])
    if not user_words:
        return False

    if config.get("user_words_position", False):
        return False

    user_words_menu = root_menu.addMenu("User Words")
    for word in user_words:
        _add_action(
            user_words_menu,
            word,
            lambda _checked=False, w=word, ctx=context_name: dispatch_user_word(web, w, ctx),
        )
    return True


def build_context_menu(parent_menu: QMenu, context_name: str, web: AnkiWebView) -> None:
    config = load_config()
    quick_specs = _quick_access_specs(config, context_name)

    quick_access_on_first_level = bool(config.get("quick_access_position", False))
    if quick_access_on_first_level and quick_specs:
        for spec in quick_specs:
            _add_spec_action(parent_menu, web, spec, context_name)
        parent_menu.addSeparator()

    if _add_user_words_first_level(config, parent_menu, web, context_name):
        parent_menu.addSeparator()

    root_menu = parent_menu.addMenu("Text Tools")

    if (not quick_access_on_first_level) and quick_specs:
        for spec in quick_specs:
            _add_spec_action(root_menu, web, spec, context_name)
        root_menu.addSeparator()

    if _add_user_words_submenu(config, root_menu, web, context_name):
        root_menu.addSeparator()

    style_presets_menu = root_menu.addMenu("Style Presets")
    for section_index, section in enumerate(STYLE_PRESET_SECTIONS):
        if section_index > 0:
            style_presets_menu.addSeparator()
        for label in section:
            spec = _spec_by_label_for_context(context_name, label)
            if spec:
                _add_spec_action(style_presets_menu, web, spec, context_name)

    root_menu.addSeparator()

    text_styling_menu = root_menu.addMenu("Text Styling")
    for spec in _submenu_specs(context_name, "text_styling"):
        _add_spec_action(text_styling_menu, web, spec, context_name)

    text_color_menu = root_menu.addMenu("Text Color")
    for spec in _submenu_specs(context_name, "text_color"):
        _add_spec_action(text_color_menu, web, spec, context_name)

    font_size_menu = root_menu.addMenu("Font Size")
    for spec in _submenu_specs(context_name, "font_size"):
        _add_spec_action(font_size_menu, web, spec, context_name)

    font_spec = _spec_by_label_for_context(context_name, "Font...")
    if font_spec:
        _add_spec_action(root_menu, web, font_spec, context_name)

    root_menu.addSeparator()

    alignment_menu = root_menu.addMenu("Alignment / List")
    for spec in _submenu_specs(context_name, "alignment"):
        _add_spec_action(alignment_menu, web, spec, context_name)

    word_count_spec = _spec_by_label_for_context(context_name, "Word Count")
    if word_count_spec:
        _add_spec_action(root_menu, web, word_count_spec, context_name)

    insert_menu = root_menu.addMenu("Insert")
    for spec in _category_specs(context_name, "insert"):
        _add_spec_into_menu_tree(insert_menu, spec, web, context_name)

    root_menu.addSeparator()

    edit_menu = root_menu.addMenu("Edit")
    for spec in _submenu_specs(context_name, "edit"):
        _add_spec_action(edit_menu, web, spec, context_name)

    root_menu.addSeparator()

    clear_format_spec = _spec_by_label_for_context(context_name, "Clear All Formatting")
    if clear_format_spec:
        _add_spec_action(root_menu, web, clear_format_spec, context_name)
