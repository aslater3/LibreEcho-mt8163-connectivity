#!/usr/bin/env python3
"""Run every source contract test in this directory.

Set KERNEL_SRC to a LibreEcho-Linux checkout to include the checks on the
kernel hooks this stack relies on.
"""

from pathlib import Path
import sys
import unittest


def main() -> int:
    here = Path(__file__).resolve().parent
    suite = unittest.defaultTestLoader.discover(str(here), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
