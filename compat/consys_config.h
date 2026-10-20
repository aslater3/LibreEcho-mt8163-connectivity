/* SPDX-License-Identifier: GPL-2.0-only */
/*
 * Build configuration for the out-of-tree MT8163 CONSYS stack.
 *
 * These were Kconfig symbols in drivers/misc/mediatek/Kconfig while the
 * stack lived in the LibreEcho Linux 6.1 tree.  They are fixed here to the
 * values mt8163_arm32_defconfig selected, so the sources keep their
 * CONFIG_* tests unchanged.  The kernel itself only needs
 * CONFIG_MTK_MT8163_CONSYS_HOST=y.
 */
#ifndef _MT8163_CONSYS_CONFIG_H
#define _MT8163_CONSYS_CONFIG_H

/* Read the factory Wi-Fi MAC and manufacturing data from /idme. */
#define CONFIG_IDME 1

/* Register the STP Bluetooth device as a BlueZ HCI controller (hci0). */
#define CONFIG_MTK_MT8163_BLUEZ_HCI 1

/* Radar-Puffin stock WMT antenna/coexistence bootstrap and selection. */
#define CONFIG_MTK_WIFI_ANTENNA_SWITCH 1
#define CONFIG_MTK_WIFI_ANTENNA_SELECT 1

/* Vendor project name, used for regulatory and antenna quirks. */
#define CONFIG_ARCH_MTK_PROJECT "radar"

#endif /* _MT8163_CONSYS_CONFIG_H */
