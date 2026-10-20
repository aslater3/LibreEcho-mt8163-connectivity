#ccflags-y += -I$(src)/core/include
subdir-ccflags-y += -I$(src)/linux/include \
						 -I$(src)/linux/pri/include \
						 -I$(src)/core/include \
						 -I$(src)/include \
						 -I$(src)/ \
						 -I$(src)/../../btif/common/inc \
						 -I$(src)/../../compat

ifeq ($(CONFIG_ARCH_MT6580), y)
subdir-ccflags-y += -D CFG_WMT_READ_EFUSE_VCN33
endif

# Out-of-tree build: one Makefile builds the WMT/STP core and the two STP
# character-device modules.  The flags below were previously set per
# subdirectory (core/, linux/pri/, linux/pub/, mt8163/).
ccflags-y += -D WMT_PLAT_ALPS
ccflags-y += -DWMT_CREATE_NODE_DYNAMIC=1
ccflags-y += -I$(src)/core -I$(src)/linux -I$(src)/mt8163/include
ifeq ($(CONFIG_MTK_TC1_FEATURE), y)
    ccflags-y += -DCFG_TC1_FEATURE=1
else
    ccflags-y += -DCFG_TC1_FEATURE=0
endif

obj-m += mt8163_stp_wmt.o
mt8163_stp_wmt-y := core/wmt_core.o \
		    core/wmt_ctrl.o \
		    core/wmt_func.o \
		    core/wmt_ic_soc.o \
		    core/wmt_lib.o \
		    core/wmt_conf.o \
		    core/btm_core.o \
		    core/dbg_core.o \
		    core/psm_core.o \
		    core/stp_core.o \
		    linux/pri/stp_btif.o \
		    linux/pri/stp_dbg.o \
		    linux/pri/stp_exp.o \
		    linux/pri/wmt_dev.o \
		    linux/pri/wmt_exp.o \
		    linux/pub/osal.o \
		    linux/pub/bgw_desense.o \
		    linux/pub/wmt_idc.o \
		    mt8163/mtk_wcn_consys_hw.o \
		    mt8163/wmt_plat_alps.o

obj-m += mt8163_stp_bt.o
mt8163_stp_bt-y := linux/pub/stp_chrdev_bt.o

obj-m += mt8163_wmt_wifi.o
mt8163_wmt_wifi-y := linux/pub/wmt_chrdev_wifi.o
