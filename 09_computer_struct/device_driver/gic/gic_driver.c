// SPDX-License-Identifier: GPL-2.0-only
/*
 * Copyright (C) 2024 Your Company Name
 * Author: Your Name <your.email@example.com>
 *
 * ARM Generic Interrupt Controller (GICv3) Driver Framework
 */

#define pr_fmt(fmt)	"arm-gic-v3: " fmt

#include <linux/init.h>
#include <linux/interrupt.h>
#include <linux/io.h>
#include <linux/irqchip.h>
#include <linux/irqchip/arm-gic-v3.h>
#include <linux/irqdomain.h>
#include <linux/of.h>
#include <linux/of_address.h>
#include <linux/percpu.h>
#include <linux/slab.h>
#include <asm/cputype.h>
#include <asm/exception.h>

/* =====================================================================
 * 1. 私有数据结构定义
 * ===================================================================== */

/**
 * struct gic_chip_data - GIC 控制器私有数据
 * @dist_base:      Distributor (GICD) MMIO 基地址
 * @redist_base:    Redistributor (GICR) per-cpu MMIO 基地址
 * @nr_irqs:        支持的中断总数
 * @domain:         关联的 irq_domain
 */
struct gic_chip_data {
	void __iomem		*dist_base;
	void __iomem __percpu	*redist_base;
	u32			nr_irqs;
	struct irq_domain	*domain;
};

static struct gic_chip_data gic_data __read_mostly;

/* =====================================================================
 * 2. 寄存器访问辅助函数
 * ===================================================================== */

static inline void __iomem *gic_dist_base(struct gic_chip_data *data)
{
	return data->dist_base;
}

static u32 gic_read_reg(void __iomem *addr, u32 offset)
{
	return readl_relaxed(addr + offset);
}

static void gic_write_reg(void __iomem *addr, u32 offset, u32 val)
{
	writel_relaxed(val, addr + offset);
}

/* =====================================================================
 * 3. irq_chip 回调实现
 * ===================================================================== */

static void gic_mask_irq(struct irq_data *d)
{
	struct gic_chip_data *data = irq_data_get_irq_chip_data(d);
	u32 reg_offset = GICD_ICENABLER + (d->hwirq / 32) * 4;
	u32 bit = BIT(d->hwirq % 32);

	gic_write_reg(data->dist_base, reg_offset, bit);
}

static void gic_unmask_irq(struct irq_data *d)
{
	struct gic_chip_data *data = irq_data_get_irq_chip_data(d);
	u32 reg_offset = GICD_ISENABLER + (d->hwirq / 32) * 4;
	u32 bit = BIT(d->hwirq % 32);

	gic_write_reg(data->dist_base, reg_offset, bit);
}

static int gic_set_affinity(struct irq_data *d, const struct cpumask *mask,
			    bool force)
{
	/* TODO: 根据目标 CPU 更新 GICD_IROUTERn 或 GICR_TYPER */
	return IRQ_SET_MASK_OK_DONE;
}

static void gic_eoi_irq(struct irq_data *d)
{
	/* GICv3 通过系统寄存器 ICC_EOIR1_EL1 完成中断 */
	gic_write_eoir(d->hwirq);
}

static struct irq_chip gic_chip = {
	.name			= "GICv3",
	.irq_mask		= gic_mask_irq,
	.irq_unmask		= gic_unmask_irq,
	.irq_eoi		= gic_eoi_irq,
	.irq_set_affinity	= gic_set_affinity,
	.flags			= IRQCHIP_SET_TYPE_MASKED |
				  IRQCHIP_SKIP_SET_WAKE |
				  IRQCHIP_MASK_ON_SUSPEND,
};

/* =====================================================================
 * 4. irq_domain_ops 实现
 * ===================================================================== */

static int gic_irq_domain_map(struct irq_domain *d, unsigned int virq,
			      irq_hw_number_t hw)
{
	if (hw >= 8192) {
		/* LPI 使用独立映射路径 */
		return -EPERM;
	}

	irq_domain_set_info(d, virq, hw, &gic_chip, d->host_data,
			    handle_fasteoi_irq, NULL, NULL);
	irq_set_probe(virq);
	return 0;
}

static const struct irq_domain_ops gic_irq_domain_ops = {
	.map	= gic_irq_domain_map,
	.xlate	= irq_domain_xlate_fourcell,
};

/* =====================================================================
 * 5. 硬件初始化
 * ===================================================================== */

static int __init gic_of_init(struct device_node *node,
			      struct device_node *parent)
{
	struct gic_chip_data *data = &gic_data;
	void __iomem *dist_base;
	void __iomem __percpu *redist_base;
	int ret;

	/* 1. 映射 GICD 寄存器 */
	dist_base = of_iomap(node, 0);
	if (!dist_base) {
		pr_err("Failed to map GICD region\n");
		return -ENOMEM;
	}

	/* 2. 映射 GICR 寄存器 */
	redist_base = of_io_request_and_map(node, 1, "gic-rdist");
	if (IS_ERR(redist_base)) {
		pr_err("Failed to map GICR region\n");
		iounmap(dist_base);
		return PTR_ERR(redist_base);
	}

	data->dist_base = dist_base;
	data->redist_base = redist_base;

	/* 3. 读取中断数量 */
	data->nr_irqs = gic_read_reg(dist_base, GICD_TYPER) & 0x1f;
	data->nr_irqs = (data->nr_irqs + 1) * 32;
	pr_info("Detected %u interrupts\n", data->nr_irqs);

	/* 4. 创建线性 irq_domain */
	data->domain = irq_domain_add_linear(node, data->nr_irqs,
					     &gic_irq_domain_ops, data);
	if (!data->domain) {
		pr_err("Failed to create irq domain\n");
		ret = -ENOMEM;
		goto err_unmap;
	}

	/* 5. 设置默认域并初始化 GICD/GICR */
	irq_set_default_host(data->domain);
	set_handle_irq(gic_handle_irq);

	pr_info("GICv3 driver initialized successfully\n");
	return 0;

err_unmap:
	iounmap(dist_base);
	iounmap((void __iomem *)redist_base);
	return ret;
}

IRQCHIP_DECLARE(arm_gic_v3, "arm,gic-v3", gic_of_init);