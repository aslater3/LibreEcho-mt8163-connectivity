/* SPDX-License-Identifier: GPL-2.0-only */
/*
 * Kernel API differences between the LTS releases this stack builds
 * against.  The sources use the newest spelling; older kernels get it
 * mapped back here, so a kernel bump only touches this file.
 */
#ifndef _MT8163_CONSYS_KCOMPAT_H
#define _MT8163_CONSYS_KCOMPAT_H

#include <linux/version.h>
#include <linux/device.h>
#include <linux/timer.h>

/* from_timer() was renamed timer_container_of() in 6.16. */
#ifndef timer_container_of
#define timer_container_of(var, callback_timer, timer_fieldname) \
	from_timer(var, callback_timer, timer_fieldname)
#endif

/* class_create() lost its owner argument in 6.4. */
#if LINUX_VERSION_CODE >= KERNEL_VERSION(6, 4, 0)
#define mt8163_class_create(name) class_create(name)
#else
#define mt8163_class_create(name) class_create(THIS_MODULE, name)
#endif

#endif /* _MT8163_CONSYS_KCOMPAT_H */
