# LibreEcho MT8163 connectivity

Out-of-tree kernel modules for the MT8163 integrated CONSYS connectivity
stack used by LibreEcho Radar-Puffin: WMT/STP, the BTIF transport, the STP
Bluetooth to BlueZ HCI bridge, and the vendor Wi-Fi driver. It is a forward
port of the vendor Linux 3.18 driver, about 213k lines in 236 files.

This code was previously built into the kernel from
`drivers/misc/mediatek/mt8163-connectivity` in
[LibreEcho-Linux-6.1](https://github.com/aslater3/LibreEcho-Linux-6.1).
Its history was carried over with `git filter-repo`, so `git log` and
`git blame` still work. Pull request numbers in older commit messages
(`#4`, `#51`, ...) refer to that repository.

It was moved out of the kernel tree so that kernel updates (6.1.y stable
merges, and later the next LTS) do not touch it. Kernel API differences
are handled in [`compat/kcompat.h`](compat/kcompat.h).

## Modules

| Module | Sources | Purpose |
|---|---|---|
| `mt8163_wmt_detect` | `compat/` | `/dev/wmtdetect` ABI and combo stub |
| `mt8163_btif` | `btif/common/` | BTIF UART/DMA transport |
| `mt8163_stp_wmt` | `conn_soc/common/{core,linux,mt8163}` | WMT/STP core and MT8163 platform |
| `mt8163_stp_bt` | `conn_soc/common/linux/pub/stp_chrdev_bt.c` | `/dev/stpbt` and the BlueZ `hci0` bridge |
| `mt8163_wmt_wifi` | `conn_soc/common/linux/pub/wmt_chrdev_wifi.c` | `/dev/wmtWifi` power control |
| `mt8163_wlan` | `conn_soc/drv_wlan/` | Wi-Fi driver (`wlan0`) |

[`modules.load`](modules.load) lists them in dependency order.

The build configuration that `mt8163_arm32_defconfig` used to select through
Kconfig (IDME factory MAC, BlueZ HCI bridge, antenna switch/select, project
name) is now fixed in [`compat/consys_config.h`](compat/consys_config.h).

## Building

You need a configured and built
[LibreEcho-Linux](https://github.com/aslater3/LibreEcho-Linux) tree with
`CONFIG_MODULES=y` and `CONFIG_MTK_MT8163_CONSYS_HOST=y` (the
`mt8163_arm32_defconfig` default). That option builds in the wireless
extensions and other infrastructure the modules cannot select themselves.

```sh
make -C /path/to/LibreEcho-Linux O=/path/to/kernel-out ARCH=arm \
  CROSS_COMPILE=arm-linux-gnueabihf- LD=arm-linux-gnueabihf-ld.bfd zImage modules
make KDIR=/path/to/kernel-out ARCH=arm \
  CROSS_COMPILE=arm-linux-gnueabihf- LD=arm-linux-gnueabihf-ld.bfd
```

## Tests

```sh
python3 -B tests/run.py
KERNEL_SRC=/path/to/LibreEcho-Linux python3 -B tests/run.py
```

These are source contract tests. With `KERNEL_SRC` set, they also check
the kernel hooks the stack relies on: the cfg80211 fallback in wext-core and
`HCI_QUIRK_DEFERRED_SETUP`. Passing them does not replace Wi-Fi association,
BlueZ pairing or recovery testing on hardware.

## Differences from the built-in driver

Every object is compiled from the same sources with the same defines as the
in-tree 6.1 build. These things did change, and need hardware acceptance
before a release ships them:

- **Init order.** Built in, the initcalls ran in this order: `wmt_detect`,
  BTIF, the BT and Wi-Fi character devices, and the WLAN driver, all at
  device level, then `WMT_init` at late initcall. As modules, `WMT_init`
  runs when `mt8163_stp_wmt` loads, which is before the BT, Wi-Fi and WLAN
  modules.
- **Loading.** Userspace (the LibreEcho-Platform initramfs) has to install
  and load the modules, in the order given by `modules.load`, before it
  starts the WMT launcher.
- **Module plumbing.** Two cross-module symbols are now exported, the
  WMT detect objects declare a license, and the AHB platform remove
  callback is no longer `__exit`.

## CI

`.github/workflows/build.yml` builds the modules against LibreEcho-Linux
`main` and fails on any modpost error. A nightly job also compiles them
against the latest stable release of the next LTS (6.18 at present). That
job only reports: a failure there is the remaining port work.
