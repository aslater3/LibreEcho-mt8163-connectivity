#!/usr/bin/env python3
"""The out-of-tree build produces the modules that modules.load lists."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
LOAD_ORDER = ROOT / "modules.load"


def built_modules() -> set:
    names = set()
    for makefile in ROOT.rglob("Makefile"):
        if makefile.parent == ROOT:
            continue
        text = makefile.read_text()
        module_name = re.search(r"^MODULE_NAME := (\S+)$", text, re.M)
        for target in re.findall(r"^obj-m \+= (\S+)\.o$", text, re.M):
            if target == "$(MODULE_NAME)" and module_name:
                target = module_name.group(1)
            names.add(target)
    return names


class ModuleLayoutTests(unittest.TestCase):
    def test_load_order_lists_every_built_module_once(self) -> None:
        lines = [
            line
            for line in LOAD_ORDER.read_text().splitlines()
            if line and not line.startswith("#")
        ]
        self.assertEqual(len(lines), len(set(lines)))
        self.assertEqual(set(lines), built_modules())

    def test_former_kconfig_choices_are_fixed(self) -> None:
        config = (ROOT / "compat/consys_config.h").read_text()
        for define in (
            "#define CONFIG_IDME 1",
            "#define CONFIG_MTK_MT8163_BLUEZ_HCI 1",
            "#define CONFIG_MTK_WIFI_ANTENNA_SWITCH 1",
            "#define CONFIG_MTK_WIFI_ANTENNA_SELECT 1",
            '#define CONFIG_ARCH_MTK_PROJECT "radar"',
        ):
            with self.subTest(define=define):
                self.assertIn(define + "\n", config)


if __name__ == "__main__":
    unittest.main()
