from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

CTX_BOTH = frozenset({"editor", "reviewer"})


@dataclass(frozen=True)
class CommandSpec:
    id: str
    label: str
    action: str
    arg: Any = None
    category: str = ""
    submenu_path: tuple[str, ...] = field(default_factory=tuple)
    contexts: frozenset[str] = field(default_factory=lambda: CTX_BOTH)
    quick_access_allowed: bool = False


def cmd(
    id: str,
    label: str,
    action: str,
    arg: Any = None,
    *,
    category: str,
    submenu_path: tuple[str, ...] = (),
    contexts: frozenset[str] = CTX_BOTH,
    quick_access_allowed: bool = False,
) -> CommandSpec:
    return CommandSpec(
        id=id,
        label=label,
        action=action,
        arg=arg,
        category=category,
        submenu_path=submenu_path,
        contexts=contexts,
        quick_access_allowed=quick_access_allowed,
    )


STYLE_PRESET_LABELS = [
    "Strong Emphasis (Bold + Underline)",
    "Important (Bold + Red)",
    "Key Point (Bold + Yellow Highlight)",
    "Alert (Bold + Red + Yellow Highlight)",
    "Underlined Attention (Underline + Red)",
    "Blue Emphasis (Bold + Blue)",
    "Green Emphasis (Bold + Green)",
    "Marked Attention (Bold + Magenta)",
    "Heading Large (Bold + x-large)",
    "Large Emphasis (Bold + Red + xx-large)",
    "Side Note (Cyan + small)",
]

CORE_QUICK_ACCESS_GROUPS: list[tuple[str, list[str]]] = [
    ("Style Presets", STYLE_PRESET_LABELS),
    (
        "Text Styling",
        [
            "Bold",
            "Italic",
            "Underline",
            "Strikethrough",
            "Small Text",
            "Superscript",
            "Subscript",
            "Monospace",
            "Inline Code",
        ],
    ),
    (
        "Text Color",
        [
            "Red",
            "Green",
            "Blue",
            "Cyan",
            "Magenta",
            "Yellow",
            "Black",
            "White",
            "Highlight Red",
            "Highlight Green",
            "Highlight Blue",
            "Highlight Cyan",
            "Highlight Magenta",
            "Highlight Yellow",
            "Highlight Black",
            "Highlight White",
        ],
    ),
    ("Font Size", ["X-Small", "Small", "Medium", "Large", "X-Large", "XX-Large", "XXX-Large"]),
    (
        "Alignment / List",
        [
            "Justify Left",
            "Justify Center",
            "Justify Right",
            "Justify Full",
            "Indent",
            "Outdent",
            "Insert Unordered List",
            "Insert Ordered List",
        ],
    ),
    (
        "Edit",
        [
            "Cut",
            "Copy",
            "Paste",
            "Paste Plain Text",
            "Remove Link",
            "Select All",
            "Undo",
            "Redo",
        ],
    ),
    ("Clear Formatting", ["Clear All Formatting"]),
]

INSERT_QUICK_ACCESS_GROUPS: list[tuple[str, list[str]]] = [
    ("Insert Helpers", ["Insert Link", "Insert Image", "Insert Ruby"]),
    (
        "Date / Time",
        [
            "YYYY-MM-DD",
            "MM/DD/YYYY",
            "Month DD, YYYY",
            "Day, Month DD, YYYY",
            "hh:mm AM/PM",
            "HH:mm",
            "HH:mm:ss",
            "YYYY-MM-DD HH:mm",
            "YYYY/MM/DD HH:mm:ss",
        ],
    ),
    (
        "Math",
        [
            "MathJax Inline",
            "MathJax Display",
            "Chemistry Inline (mhchem)",
            "Chemistry Display (mhchem)",
            "LaTeX",
        ],
    ),
    ("Structure", ["Blockquote", "Horizontal Line"]),
]

SPECIAL_CHARACTER_GROUPS: list[tuple[str, list[tuple[str, str, str]]]] = [
    (
        "Typography",
        [
            ("special_em_dash", "Em Dash (—)", "—"),
            ("special_en_dash", "En Dash (–)", "–"),
            ("special_hbar", "Horizontal Bar (―)", "―"),
            ("special_ellipsis", "Ellipsis (…)", "…"),
            ("special_bullet", "Bullet (•)", "•"),
            ("special_middle_dot", "Middle Dot (·)", "·"),
            ("special_japanese_middle_dot", "Japanese Middle Dot (・)", "・"),
            ("special_double_low_line", "Double Low Line (‗)", "‗"),
        ],
    ),
    (
        "Arrows / Marks",
        [
            ("special_arrow_right", "Right Arrow (→)", "→"),
            ("special_arrow_left", "Left Arrow (←)", "←"),
            ("special_arrow_up", "Up Arrow (↑)", "↑"),
            ("special_arrow_down", "Down Arrow (↓)", "↓"),
            ("special_arrow_lr", "Left-Right Arrow (↔)", "↔"),
            ("special_double_arrow_right", "Double Right Arrow (⇒)", "⇒"),
            ("special_double_arrow_lr", "Double Left-Right Arrow (⇔)", "⇔"),
            ("special_check_mark", "Check Mark (✓)", "✓"),
            ("special_cross_mark", "Cross Mark (✗)", "✗"),
            ("special_reference_mark", "Reference Mark (※)", "※"),
        ],
    ),
    (
        "Math / Technical Symbols",
        [
            ("special_plus_minus", "Plus-Minus (±)", "±"),
            ("special_multiplication", "Multiplication (×)", "×"),
            ("special_division", "Division (÷)", "÷"),
            ("special_not_equal", "Not Equal (≠)", "≠"),
            ("special_leq", "Less Than or Equal (≤)", "≤"),
            ("special_geq", "Greater Than or Equal (≥)", "≥"),
            ("special_approx", "Approximately Equal (≈)", "≈"),
            ("special_infinity", "Infinity (∞)", "∞"),
            ("special_degree", "Degree (°)", "°"),
            ("special_micro", "Micro (µ)", "µ"),
            ("special_not", "Not (¬)", "¬"),
        ],
    ),
    (
        "Legal / Reference",
        [
            ("special_section", "Section (§)", "§"),
            ("special_pilcrow", "Pilcrow (¶)", "¶"),
            ("special_numero", "Numero Sign (№)", "№"),
            ("special_copyright", "Copyright (©)", "©"),
            ("special_registered", "Registered (®)", "®"),
            ("special_trademark", "Trademark (™)", "™"),
        ],
    ),
    (
        "Currency / Units",
        [
            ("special_yen", "Yen/Yuan (¥)", "¥"),
            ("special_euro", "Euro (€)", "€"),
            ("special_pound", "Pound (£)", "£"),
            ("special_cent", "Cent (¢)", "¢"),
            ("special_celsius", "Celsius (℃)", "℃"),
            ("special_fahrenheit", "Fahrenheit (℉)", "℉"),
            ("special_ohm", "Ohm (Ω)", "Ω"),
        ],
    ),
]

SPECIAL_CHARACTER_QUICK_ACCESS_GROUPS: list[tuple[str, list[str]]] = [
    (group_name, [label for _id, label, _char in items])
    for group_name, items in SPECIAL_CHARACTER_GROUPS
]

COMMANDS: list[CommandSpec] = [
    # Text Styling
    cmd(
        "bold", "Bold", "wrap_tag", {"tag": "b"}, category="text_styling", quick_access_allowed=True
    ),
    cmd(
        "italic",
        "Italic",
        "wrap_tag",
        {"tag": "i"},
        category="text_styling",
        quick_access_allowed=True,
    ),
    cmd(
        "underline",
        "Underline",
        "wrap_tag",
        {"tag": "u"},
        category="text_styling",
        quick_access_allowed=True,
    ),
    cmd(
        "strikethrough",
        "Strikethrough",
        "wrap_tag",
        {"tag": "s"},
        category="text_styling",
        quick_access_allowed=True,
    ),
    cmd(
        "small_text",
        "Small Text",
        "apply_style",
        {"fontSize": "small"},
        category="text_styling",
        quick_access_allowed=True,
    ),
    cmd(
        "superscript",
        "Superscript",
        "wrap_tag",
        {"tag": "sup"},
        category="text_styling",
        quick_access_allowed=True,
    ),
    cmd(
        "subscript",
        "Subscript",
        "wrap_tag",
        {"tag": "sub"},
        category="text_styling",
        quick_access_allowed=True,
    ),
    cmd(
        "monospace",
        "Monospace",
        "apply_style",
        {"fontFamily": "monospace"},
        category="text_styling",
        quick_access_allowed=True,
    ),
    cmd(
        "inline_code",
        "Inline Code",
        "apply_style",
        {"fontFamily": "monospace", "backgroundColor": "#f5f5f5"},
        category="text_styling",
        quick_access_allowed=True,
    ),
    # Text Color
    cmd(
        "red",
        "Red",
        "apply_style",
        {"color": "red"},
        category="text_color",
        quick_access_allowed=True,
    ),
    cmd(
        "green",
        "Green",
        "apply_style",
        {"color": "green"},
        category="text_color",
        quick_access_allowed=True,
    ),
    cmd(
        "blue",
        "Blue",
        "apply_style",
        {"color": "blue"},
        category="text_color",
        quick_access_allowed=True,
    ),
    cmd(
        "cyan",
        "Cyan",
        "apply_style",
        {"color": "cyan"},
        category="text_color",
        quick_access_allowed=True,
    ),
    cmd(
        "magenta",
        "Magenta",
        "apply_style",
        {"color": "magenta"},
        category="text_color",
        quick_access_allowed=True,
    ),
    cmd(
        "yellow",
        "Yellow",
        "apply_style",
        {"color": "yellow"},
        category="text_color",
        quick_access_allowed=True,
    ),
    cmd(
        "black",
        "Black",
        "apply_style",
        {"color": "black"},
        category="text_color",
        quick_access_allowed=True,
    ),
    cmd(
        "white",
        "White",
        "apply_style",
        {"color": "white"},
        category="text_color",
        quick_access_allowed=True,
    ),
    cmd(
        "back_red",
        "Highlight Red",
        "apply_style",
        {"backgroundColor": "red"},
        category="text_color",
        quick_access_allowed=True,
    ),
    cmd(
        "back_green",
        "Highlight Green",
        "apply_style",
        {"backgroundColor": "green"},
        category="text_color",
        quick_access_allowed=True,
    ),
    cmd(
        "back_blue",
        "Highlight Blue",
        "apply_style",
        {"backgroundColor": "blue"},
        category="text_color",
        quick_access_allowed=True,
    ),
    cmd(
        "back_cyan",
        "Highlight Cyan",
        "apply_style",
        {"backgroundColor": "cyan"},
        category="text_color",
        quick_access_allowed=True,
    ),
    cmd(
        "back_magenta",
        "Highlight Magenta",
        "apply_style",
        {"backgroundColor": "magenta"},
        category="text_color",
        quick_access_allowed=True,
    ),
    cmd(
        "back_yellow",
        "Highlight Yellow",
        "apply_style",
        {"backgroundColor": "yellow"},
        category="text_color",
        quick_access_allowed=True,
    ),
    cmd(
        "back_black",
        "Highlight Black",
        "apply_style",
        {"backgroundColor": "black"},
        category="text_color",
        quick_access_allowed=True,
    ),
    cmd(
        "back_white",
        "Highlight White",
        "apply_style",
        {"backgroundColor": "white"},
        category="text_color",
        quick_access_allowed=True,
    ),
    # Font Size
    cmd(
        "size_1",
        "X-Small",
        "apply_style",
        {"fontSize": "x-small"},
        category="font_size",
        quick_access_allowed=True,
    ),
    cmd(
        "size_2",
        "Small",
        "apply_style",
        {"fontSize": "small"},
        category="font_size",
        quick_access_allowed=True,
    ),
    cmd(
        "size_3",
        "Medium",
        "apply_style",
        {"fontSize": "medium"},
        category="font_size",
        quick_access_allowed=True,
    ),
    cmd(
        "size_4",
        "Large",
        "apply_style",
        {"fontSize": "large"},
        category="font_size",
        quick_access_allowed=True,
    ),
    cmd(
        "size_5",
        "X-Large",
        "apply_style",
        {"fontSize": "x-large"},
        category="font_size",
        quick_access_allowed=True,
    ),
    cmd(
        "size_6",
        "XX-Large",
        "apply_style",
        {"fontSize": "xx-large"},
        category="font_size",
        quick_access_allowed=True,
    ),
    cmd(
        "size_7",
        "XXX-Large",
        "apply_style",
        {"fontSize": "xxx-large"},
        category="font_size",
        quick_access_allowed=True,
    ),
    # Font
    cmd("font_dialog", "Font...", "font_dialog", category="font"),
    # Style Presets
    cmd(
        "preset_strong_emphasis",
        "Strong Emphasis (Bold + Underline)",
        "apply_style",
        {"fontWeight": "bold", "textDecoration": "underline"},
        category="style_presets",
        quick_access_allowed=True,
    ),
    cmd(
        "preset_important",
        "Important (Bold + Red)",
        "apply_style",
        {"fontWeight": "bold", "color": "red"},
        category="style_presets",
        quick_access_allowed=True,
    ),
    cmd(
        "preset_key_point",
        "Key Point (Bold + Yellow Highlight)",
        "apply_style",
        {"fontWeight": "bold", "backgroundColor": "yellow"},
        category="style_presets",
        quick_access_allowed=True,
    ),
    cmd(
        "preset_alert",
        "Alert (Bold + Red + Yellow Highlight)",
        "apply_style",
        {"fontWeight": "bold", "color": "red", "backgroundColor": "yellow"},
        category="style_presets",
        quick_access_allowed=True,
    ),
    cmd(
        "preset_underlined_attention",
        "Underlined Attention (Underline + Red)",
        "apply_style",
        {"textDecoration": "underline", "color": "red"},
        category="style_presets",
        quick_access_allowed=True,
    ),
    cmd(
        "preset_blue_emphasis",
        "Blue Emphasis (Bold + Blue)",
        "apply_style",
        {"fontWeight": "bold", "color": "blue"},
        category="style_presets",
        quick_access_allowed=True,
    ),
    cmd(
        "preset_green_emphasis",
        "Green Emphasis (Bold + Green)",
        "apply_style",
        {"fontWeight": "bold", "color": "green"},
        category="style_presets",
        quick_access_allowed=True,
    ),
    cmd(
        "preset_marked_attention",
        "Marked Attention (Bold + Magenta)",
        "apply_style",
        {"fontWeight": "bold", "color": "magenta"},
        category="style_presets",
        quick_access_allowed=True,
    ),
    cmd(
        "preset_heading_large",
        "Heading Large (Bold + x-large)",
        "apply_style",
        {"fontWeight": "bold", "fontSize": "x-large"},
        category="style_presets",
        quick_access_allowed=True,
    ),
    cmd(
        "preset_large_emphasis",
        "Large Emphasis (Bold + Red + xx-large)",
        "apply_style",
        {"fontWeight": "bold", "color": "red", "fontSize": "xx-large"},
        category="style_presets",
        quick_access_allowed=True,
    ),
    cmd(
        "preset_side_note",
        "Side Note (Cyan + small)",
        "apply_style",
        {"color": "cyan", "fontSize": "small"},
        category="style_presets",
        quick_access_allowed=True,
    ),
    # Alignment / List
    cmd(
        "justify_left",
        "Justify Left",
        "block_style",
        {"textAlign": "left"},
        category="alignment",
        quick_access_allowed=True,
    ),
    cmd(
        "justify_center",
        "Justify Center",
        "block_style",
        {"textAlign": "center"},
        category="alignment",
        quick_access_allowed=True,
    ),
    cmd(
        "justify_right",
        "Justify Right",
        "block_style",
        {"textAlign": "right"},
        category="alignment",
        quick_access_allowed=True,
    ),
    cmd(
        "justify_full",
        "Justify Full",
        "block_style",
        {"textAlign": "justify"},
        category="alignment",
        quick_access_allowed=True,
    ),
    cmd("indent", "Indent", "indent", category="alignment", quick_access_allowed=True),
    cmd("outdent", "Outdent", "outdent", category="alignment", quick_access_allowed=True),
    cmd(
        "insert_unordered_list",
        "Insert Unordered List",
        "insert_list",
        {"ordered": False},
        category="alignment",
        quick_access_allowed=True,
    ),
    cmd(
        "insert_ordered_list",
        "Insert Ordered List",
        "insert_list",
        {"ordered": True},
        category="alignment",
        quick_access_allowed=True,
    ),
    # Tools
    cmd("word_count", "Word Count", "word_count", category="tools"),
    # Insert
    cmd(
        "insert_link",
        "Insert Link",
        "insert_link_prompt",
        category="insert",
        quick_access_allowed=True,
    ),
    cmd(
        "insert_image",
        "Insert Image",
        "insert_image_prompt",
        category="insert",
        quick_access_allowed=True,
    ),
    cmd(
        "insert_ruby",
        "Insert Ruby",
        "insert_ruby_prompt",
        category="insert",
        quick_access_allowed=True,
    ),
    # Insert Date and Time
    cmd(
        "date_ymd",
        "YYYY-MM-DD",
        "insert_datetime",
        "%Y-%m-%d",
        category="insert",
        submenu_path=("Insert Date and Time",),
        quick_access_allowed=True,
    ),
    cmd(
        "date_mdy",
        "MM/DD/YYYY",
        "insert_datetime",
        "%m/%d/%Y",
        category="insert",
        submenu_path=("Insert Date and Time",),
        quick_access_allowed=True,
    ),
    cmd(
        "date_month_dd_yyyy",
        "Month DD, YYYY",
        "insert_datetime",
        "%B %d, %Y",
        category="insert",
        submenu_path=("Insert Date and Time",),
        quick_access_allowed=True,
    ),
    cmd(
        "date_day_month_dd_yyyy",
        "Day, Month DD, YYYY",
        "insert_datetime",
        "%A, %B %d, %Y",
        category="insert",
        submenu_path=("Insert Date and Time",),
        quick_access_allowed=True,
    ),
    cmd(
        "time_ampm",
        "hh:mm AM/PM",
        "insert_datetime",
        "%I:%M %p",
        category="insert",
        submenu_path=("Insert Date and Time",),
        quick_access_allowed=True,
    ),
    cmd(
        "time_24h",
        "HH:mm",
        "insert_datetime",
        "%H:%M",
        category="insert",
        submenu_path=("Insert Date and Time",),
        quick_access_allowed=True,
    ),
    cmd(
        "time_24h_seconds",
        "HH:mm:ss",
        "insert_datetime",
        "%H:%M:%S",
        category="insert",
        submenu_path=("Insert Date and Time",),
        quick_access_allowed=True,
    ),
    cmd(
        "datetime_ymd_hm",
        "YYYY-MM-DD HH:mm",
        "insert_datetime",
        "%Y-%m-%d %H:%M",
        category="insert",
        submenu_path=("Insert Date and Time",),
        quick_access_allowed=True,
    ),
    cmd(
        "datetime_slash_ymd_hms",
        "YYYY/MM/DD HH:mm:ss",
        "insert_datetime",
        "%Y/%m/%d %H:%M:%S",
        category="insert",
        submenu_path=("Insert Date and Time",),
        quick_access_allowed=True,
    ),
    # Insert Math
    cmd(
        "mathjax_inline",
        "MathJax Inline",
        "insert_text",
        "\\(\u200b\\)",
        category="insert",
        submenu_path=("Insert Math",),
        quick_access_allowed=True,
    ),
    cmd(
        "mathjax_display",
        "MathJax Display",
        "insert_text",
        "\\[\n\u200b\n\\]",
        category="insert",
        submenu_path=("Insert Math",),
        quick_access_allowed=True,
    ),
    cmd(
        "chem_inline",
        "Chemistry Inline (mhchem)",
        "insert_text",
        "\\(\\ce{\u200b}\\)",
        category="insert",
        submenu_path=("Insert Math",),
        quick_access_allowed=True,
    ),
    cmd(
        "chem_display",
        "Chemistry Display (mhchem)",
        "insert_text",
        "\\[\n\\ce{\u200b}\n\\]",
        category="insert",
        submenu_path=("Insert Math",),
        quick_access_allowed=True,
    ),
    cmd(
        "latex_block",
        "LaTeX",
        "insert_text",
        "[latex]\u200b[/latex]",
        category="insert",
        submenu_path=("Insert Math",),
        quick_access_allowed=True,
    ),
    # Insert Structure
    cmd(
        "insert_blockquote",
        "Blockquote",
        "insert_blockquote",
        category="insert",
        submenu_path=("Insert Structure",),
        quick_access_allowed=True,
    ),
    cmd(
        "insert_horizontal_rule",
        "Horizontal Line",
        "insert_html",
        "<hr>",
        category="insert",
        submenu_path=("Insert Structure",),
        quick_access_allowed=True,
    ),
    # Edit
    cmd("cut", "Cut", "cut", category="edit", quick_access_allowed=True),
    cmd("copy", "Copy", "copy", category="edit", quick_access_allowed=True),
    cmd("paste", "Paste", "paste", category="edit", quick_access_allowed=True),
    cmd(
        "paste_plain_text",
        "Paste Plain Text",
        "paste_plain_text",
        category="edit",
        quick_access_allowed=True,
    ),
    cmd("remove_link", "Remove Link", "remove_link", category="edit", quick_access_allowed=True),
    cmd("select_all", "Select All", "select_all", category="edit", quick_access_allowed=True),
    cmd("undo", "Undo", "undo", category="edit", quick_access_allowed=True),
    cmd("redo", "Redo", "redo", category="edit", quick_access_allowed=True),
    # Clear
    cmd(
        "clear_format",
        "Clear All Formatting",
        "clear_format",
        category="clear_format",
        quick_access_allowed=True,
    ),
]

# Insert Special Characters
for group_name, items in SPECIAL_CHARACTER_GROUPS:
    for item_id, label, char in items:
        COMMANDS.append(
            cmd(
                item_id,
                label,
                "insert_text",
                char,
                category="insert",
                submenu_path=("Insert Special Characters", group_name),
                quick_access_allowed=True,
            )
        )

# Insert Table
TABLE_COMMANDS: list[CommandSpec] = []
for with_header, header_label in ((False, "No Header"), (True, "With Header")):
    for rows in range(1, 11):
        row_label = f"{rows} Row" if rows == 1 else f"{rows} Rows"
        for cols in range(1, 11):
            col_label = f"{cols} Col" if cols == 1 else f"{cols} Cols"
            TABLE_COMMANDS.append(
                cmd(
                    id=f"table_{'with_header' if with_header else 'no_header'}_r{rows}_c{cols}",
                    label=col_label,
                    action="insert_table",
                    arg={"rows": rows, "cols": cols, "with_header": with_header},
                    category="insert",
                    submenu_path=("Insert Table", header_label, row_label),
                )
            )

insert_ruby_index = next(i for i, spec in enumerate(COMMANDS) if spec.id == "insert_ruby")
COMMANDS[insert_ruby_index + 1 : insert_ruby_index + 1] = TABLE_COMMANDS

STYLE_PRESET_SECTIONS: list[list[str]] = [
    [
        "Strong Emphasis (Bold + Underline)",
        "Important (Bold + Red)",
        "Key Point (Bold + Yellow Highlight)",
        "Alert (Bold + Red + Yellow Highlight)",
        "Underlined Attention (Underline + Red)",
    ],
    [
        "Blue Emphasis (Bold + Blue)",
        "Green Emphasis (Bold + Green)",
        "Marked Attention (Bold + Magenta)",
    ],
    [
        "Heading Large (Bold + x-large)",
        "Large Emphasis (Bold + Red + xx-large)",
        "Side Note (Cyan + small)",
    ],
]
