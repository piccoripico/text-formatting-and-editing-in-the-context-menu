from __future__ import annotations

import unittest

from helpers import load_addon_module


class MenuSpecTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_addon_module("menu_spec")

    def test_command_ids_are_unique(self) -> None:
        command_ids = [spec.id for spec in self.module.COMMANDS]
        self.assertEqual(len(command_ids), len(set(command_ids)))

    def test_quick_access_groups_only_reference_allowed_commands(self) -> None:
        quick_access_labels = {
            spec.label for spec in self.module.COMMANDS if spec.quick_access_allowed
        }
        grouped_labels = []
        for groups in (
            self.module.CORE_QUICK_ACCESS_GROUPS,
            self.module.INSERT_QUICK_ACCESS_GROUPS,
            self.module.SPECIAL_CHARACTER_QUICK_ACCESS_GROUPS,
        ):
            for _group_name, labels in groups:
                grouped_labels.extend(labels)

        missing = sorted(label for label in grouped_labels if label not in quick_access_labels)
        self.assertEqual(missing, [])

    def test_table_commands_cover_all_sizes_and_header_options(self) -> None:
        table_specs = [spec for spec in self.module.COMMANDS if spec.action == "insert_table"]

        self.assertEqual(len(table_specs), 200)
        table_ids = {spec.id for spec in table_specs}
        self.assertIn("table_no_header_r1_c1", table_ids)
        self.assertIn("table_with_header_r10_c10", table_ids)

    def test_style_preset_sections_match_declared_labels(self) -> None:
        flattened_sections = [
            label for section in self.module.STYLE_PRESET_SECTIONS for label in section
        ]
        self.assertEqual(flattened_sections, self.module.STYLE_PRESET_LABELS)

    def test_special_character_quick_access_groups_match_source_groups(self) -> None:
        expected_groups = [
            (group_name, [label for _item_id, label, _char in items])
            for group_name, items in self.module.SPECIAL_CHARACTER_GROUPS
        ]
        self.assertEqual(self.module.SPECIAL_CHARACTER_QUICK_ACCESS_GROUPS, expected_groups)


if __name__ == "__main__":
    unittest.main()
