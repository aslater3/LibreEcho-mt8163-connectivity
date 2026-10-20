#!/usr/bin/env python3
"""Source contracts for the MT8163 STP Bluetooth to BlueZ HCI bridge.

The bridge defers HCI setup until WMT is ready and depends on the kernel's
HCI_QUIRK_DEFERRED_SETUP ("Bluetooth: add HCI_QUIRK_DEFERRED_SETUP" in
LibreEcho-Linux).  That kernel half is checked when KERNEL_SRC points at the
kernel tree.
"""

import os
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DRIVER = ROOT / "conn_soc/common/linux/pub/stp_chrdev_bt.c"
CONSYS_CONFIG = ROOT / "compat/consys_config.h"
KERNEL_SRC = os.environ.get("KERNEL_SRC")


class Mt8163BluetoothBridgeContractTests(unittest.TestCase):
    def test_bluez_hci_bridge_is_built(self) -> None:
        config = CONSYS_CONFIG.read_text()
        self.assertIn("#define CONFIG_MTK_MT8163_BLUEZ_HCI 1\n", config)

    def test_deferred_registration_allows_only_power_on_during_setup(self) -> None:
        driver = DRIVER.read_text()
        self.assertIn(
            "set_bit(HCI_QUIRK_DEFERRED_SETUP, &mtk_hci.hdev->quirks);",
            driver,
        )
        self.assertNotIn("hci_dev_clear_flag(mtk_hci.hdev, HCI_SETUP);", driver)

    @unittest.skipUnless(KERNEL_SRC, "KERNEL_SRC not set")
    def test_kernel_provides_deferred_setup_quirk(self) -> None:
        kernel = Path(KERNEL_SRC)
        self.assertIn(
            "HCI_QUIRK_DEFERRED_SETUP",
            (kernel / "include/net/bluetooth/hci.h").read_text(),
        )
        self.assertIn(
            "opcode == MGMT_OP_SET_POWERED",
            (kernel / "net/bluetooth/hci_sock.c").read_text(),
        )

    def test_bridge_keeps_explicit_hci_lifecycle_contract(self) -> None:
        source = DRIVER.read_text()
        for marker in (
            "result = mtk_wcn_stp_register_if_rx(mtk_bt_hci_receive);",
            "result = mtk_wcn_stp_send_data(skb->data, skb->len,",
            "result = hci_recv_frame(mtk_hci.hdev, skb);",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, source)


if __name__ == "__main__":
    unittest.main()
