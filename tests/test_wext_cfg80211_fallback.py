#!/usr/bin/env python3
"""Source contracts for MT8163 WEXT userspace over cfg80211.

The driver exposes only private WEXT handlers on its netdev and relies on
the kernel's wext-core falling back to cfg80211 for the standard ones
("wifi: wext: fall back to cfg80211 standard handlers" in LibreEcho-Linux).
That kernel half is checked when KERNEL_SRC points at the kernel tree.
"""

import os
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
GL_INIT = ROOT / "conn_soc/drv_wlan/mt_wifi/wlan/os/linux/gl_init.c"
KERNEL_SRC = os.environ.get("KERNEL_SRC")


class WextCfg80211FallbackTests(unittest.TestCase):
    def test_driver_does_not_override_cfg80211_standard_handlers(self) -> None:
        source = GL_INIT.read_text(encoding="utf-8")
        self.assertNotIn("prWiphy->wext = &wext_handler_def", source)

    @unittest.skipUnless(KERNEL_SRC, "KERNEL_SRC not set")
    def test_kernel_falls_back_to_cfg80211_standard_handlers(self) -> None:
        source = (Path(KERNEL_SRC) / "net/wireless/wext-core.c").read_text(
            encoding="utf-8"
        )
        get_handler = source.split("static iw_handler get_handler", 1)[1].split(
            "static int ioctl_standard_iw_point", 1
        )[0]
        self.assertIn("cfg_handlers->standard[index]", get_handler)


if __name__ == "__main__":
    unittest.main()
