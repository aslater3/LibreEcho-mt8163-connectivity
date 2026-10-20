# SPDX-License-Identifier: GPL-2.0-only
#
# Out-of-tree build of the MT8163 CONSYS stack.  KDIR is a configured and
# built kernel tree (or its O= output directory) with
# CONFIG_MTK_MT8163_CONSYS_HOST=y.  Command-line variables such as ARCH,
# CROSS_COMPILE and LD are passed through to the kernel build:
#
#   make KDIR=/path/to/kernel-out ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf-

KDIR ?= /lib/modules/$(shell uname -r)/build

all: modules

modules modules_install clean:
	$(MAKE) -C $(KDIR) M=$(CURDIR) $@

test:
	python3 -B tests/run.py

.PHONY: all modules modules_install clean test
