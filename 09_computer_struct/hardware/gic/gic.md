# GIC (Generic Interrupt Controller) 技术详解

## 1. 什么是 GIC？

**GIC（通用中断控制器）** 是 ARM 架构中标准化的中断管理硬件模块，负责在处理器核心与外设之间路由、优先级排序和分发中断信号。

自 ARMv7 起，GIC 取代了各 SoC 厂商自定义的中断控制器，成为 ARM 生态系统中**统一的中断接口标准**。它定义了从外设到 CPU 的完整中断传递机制，是 Linux/RTOS 等操作系统在 ARM 平台上实现中断子系统的基础。

> 📌 **核心价值**：GIC 的存在使得同一份 OS 内核代码可以运行在不同 ARM SoC 上而无需修改中断驱动逻辑，极大提升了软件可移植性。

---

## 2. GIC 架构演进

| 版本      | 引入时间 | 关键特性                                                     | 典型应用               |
| :-------- | :------- | :----------------------------------------------------------- | :--------------------- |
| **GICv2** | ARMv7    | SPI/PPI/SGI 三类中断；Group0/Group1 安全分组；最多 8 核       | Cortex-A7/A9/A15/A53   |
| **GICv3** | ARMv8    | 支持 >8 核；Affinity Routing；LPI (ITS)；系统寄存器访问替代 MMIO | Cortex-A55/A72/A76/A78 |
| **GICv4** | ARMv8.1  | 虚拟 LPI 直接注入 vPE；减少虚拟化中断开销                     | 服务器/云计算虚拟化     |
| **GICv4.1**| ARMv8.4  | 改进 vSGI 支持；增强虚拟化管理                                | 新一代数据中心          |

> ⚠️ **注意**：GICv3/v4 不再使用 CPU Interface 的 MMIO 访问方式，改为通过 **System Registers**（如 `ICC_*` 系列）进行交互，这是与 GICv2 最显著的编程模型差异。

---

## 3. 中断类型分类

GIC 将中断分为三大类，每类有不同的来源和处理方式：

### 3.1 SGI (Software Generated Interrupt)
- **编号范围**: ID 0–15
- **触发方式**: 由软件写入 `GICD_SGIR` / `ICC_SGI1R_EL1` 触发
- **用途**: 核间通信（IPI）、调度器唤醒、TLB flush 通知
- **特点**: 仅存在于 GIC Distributor 内部，不经过外部引脚

### 3.2 PPI (Private Peripheral Interrupt)
- **编号范围**: ID 16–31
- **来源**: 每个 CPU 私有的外设（如私有定时器、PMU、CNTP/CNTV）
- **特点**: 绑定到特定核心，Distributor 按 core 独立路由

### 3.3 SPI (Shared Peripheral Interrupt)
- **编号范围**: ID 32–1019
- **来源**: 共享外设（UART、SPI、GPIO、DMA、PCIe 等）
- **路由模式**:
  - **1-N Model**: 广播到多个核心，首个响应的核心处理
  - **N-N Model (GICv3+)**: 通过 Affinity 精确指定目标核心

### 3.4 LPI (Locality-specific Peripheral Interrupt) — GICv3+
- **编号范围**: ID 8192+
- **来源**: PCIe MSI-X、平台设备通过 ITS 生成
- **特点**: 基于消息触发而非电平/边带信号；支持海量中断源（数万级）；天然适配虚拟化

---

## 4. GIC 硬件组成

```text
┌──────────────┐    ┌─────────────────┐    ┌──────────────────┐
│   外设/ITS   │───►│   Distributor   │───►│  Redistributor   │───► CPU Core
│  (SPI/LPI)   │    │   (GICD)        │    │  (GICR, per-core)│    (via SysReg)
└──────────────┘    └─────────────────┘    └──────────────────┘
                           ▲                       ▲
                           │                       │
                    ┌──────┴──────┐         ┌──────┴──────┐
                    │  GICD Base  │         │  GICR Base  │
                    │  (MMIO)     │         │  (MMIO)     │
                    └─────────────┘         └─────────────┘

```

### 4.1 Distributor (GICD)
- 全局唯一实例
- 接收所有 SPI/LPI 中断请求
- 执行优先级仲裁、安全状态过滤、目标路由决策
- 维护中断配置寄存器（使能、优先级、目标、触发模式）

### 4.2 Redistributor (GICR) — GICv3+
- 每个 CPU 核心一个实例
- 管理该核心的 PPI/SGI
- 作为 Distributor 与 CPU Interface 之间的桥梁
- 包含睡眠/唤醒状态管理（Processor Sleep）

### 4.3 CPU Interface
- **GICv2**: 通过 `GICC_*` MMIO 寄存器访问
- **GICv3+**: 通过 `ICC_*` 系统寄存器访问（性能更高，避免总线瓶颈）
- 功能：确认中断（ACK）、完成中断（EOI）、设置优先级掩码、抢占控制

### 4.4 ITS (Interrupt Translation Service) — GICv3+
- 专用于 LPI 的翻译与缓存
- 将设备发出的 MSI 消息转换为 LPI 中断号
- 维护 Device Table、Collection Table、LPI Pending Table
- 支持 Direct Injection to vPE（GICv4）

---

## 5. 中断生命周期

```text
外设产生中断信号
        │
        ▼
  Distributor 接收并锁存
        │
        ▼
  优先级仲裁 + 安全检查
        │
        ▼
  根据路由策略选择目标 CPU
        │
        ▼
  Redistributor 转发至目标 CPU Interface
        │
        ▼
  CPU Interface 比较当前优先级掩码
        │
        ├── 高于掩码 → 向 CPU 发出 nIRQ/FIQ 信号
        │
        └── 低于掩码 → 保持 pending，等待 EOI 或掩码降低
                │
                ▼
        CPU 进入异常向量表
                │
                ▼
        OS 读取 IAR → 获取 INTID + 优先级
                │
                ▼
        执行中断服务程序 (ISR)
                │
                ▼
        写入 EOIR → 通知 GIC 中断处理完成
                │
                ▼
        GIC 清除 active 状态，允许同级/低级中断响应

```

### 关键概念说明

- **Pending**: 中断已到达但尚未被 CPU 确认
- **Active**: CPU 已确认中断，正在处理中
- **Active and Pending**: 处理过程中同一中断再次触发
- **Priority Masking**: CPU Interface 屏蔽低于某优先级的中断
- **Preemption**: 高优先级中断可打断低优先级 Active 中断（需配置 Group Priority）

---

## 6. 安全模型与安全分组

GIC 支持 TrustZone 安全世界隔离：

| Group   | 安全属性     | 典型用途                     | 异常级别       |
| :------ | :----------- | :---------------------------- | :------------- |
| Group 0 | Secure FIQ   | TEE 安全监控、密钥管理        | EL3 / S-EL1    |
| Group 1S| Secure IRQ   | 安全 OS 正常中断              | S-EL1          |
| Group 1NS| Non-secure IRQ | Normal World OS 中断        | NS-EL1 / EL2   |

- **GICD_CTLR.DS** 位控制是否启用双安全域
- 非安全世界无法读写 Group 0 相关寄存器
- EL3 固件（如 TF-A）负责初始化安全分组策略

---

## 7. Linux 内核中的 GIC 驱动

### 7.1 驱动框架位置

```text
drivers/irqchip/
├── irq-gic.c          # GICv2 主驱动
├── irq-gic-v3.c       # GICv3/v4 主驱动
├── irq-gic-v3-its.c   # ITS 驱动
├── irq-gic-common.c   # 公共工具函数
└── irq-gic-v3-mbi.c   # MSI 桥接支持

```

### 7.2 设备树绑定示例 (GICv3)

```dts
gic: interrupt-controller@2c000000 {
    compatible = "arm,gic-v3";
    #interrupt-cells = <4>;
    interrupt-controller;
    reg = <0x0 0x2c000000 0 0x10000>,   /* GICD */
          <0x0 0x2c100000 0 0x200000>,  /* GICR */
          <0x0 0x2d000000 0 0x200000>;  /* ITS */
    msi-controller;
};

```

> 💡 `#interrupt-cells = <4>` 含义：`<type intid flags affinity>`，其中 type=0(SPI)/1(PPI)/2(ESPI)/3(EPPI)

### 7.3 关键内核 API

| API                          | 作用                              |
| :--------------------------- | :-------------------------------- |
| `gic_init()`                 | 早期初始化 GIC                    |
| `gic_set_affinity()`         | 设置 SPI 的目标 CPU               |
| `gic_raise_softirq()`        | 发送 SGI (IPI)                   |
| `gic_read_iar()`             | 读取当前最高优先级中断            |
| `gic_write_eoir()`           | 完成中断处理                      |
| `its_send_single_msi()`      | 通过 ITS 发送 MSI                 |

---

## 8. 调试与常见问题

### 8.1 常见故障现象

| 现象                         | 可能原因                                      |
| :--------------------------- | :-------------------------------------------- |
| 中断完全不触发               | GICD/GICR 未使能；中断线未连接；DT 配置错误   |
| 中断触发但 ISR 未执行        | 优先级掩码过高；安全分组错误；向量表未注册     |
| 中断风暴                     | 电平触发未正确清除；缺少 ACK/EOI 配对         |
| 多核下中断只在一个核响应     | Affinity 未正确设置；1-N 模式下竞争条件       |
| LPI 不工作                   | ITS 未初始化；Device Table 配置错误；MSI 地址错|
| 虚拟机收不到中断             | vGIC 未模拟；LPI Direct Injection 未启用       |

### 8.2 调试手段

1.  **查看中断统计**:
    ```bash
    cat /proc/interrupts

    ```
2.  **检查 GIC 寄存器状态** (通过 debugfs):
    ```bash
    mount -t debugfs none /sys/kernel/debug
    cat /sys/kernel/debug/gic-v3/dist_base

    ```
3.  **QEMU/GDB 调试**:
    ```bash
    (qemu) info irq
    (gdb) monitor info gic

    ```
4.  **TF-A / U-Boot 日志**: 确认 EL3 阶段 GIC 初始化是否正确
5.  **硬件手册对照**: 核实 DT 中 base address、size、interrupt-cells 是否与 TRM 一致

### 8.3 易错点提醒

- GICv3 的 CPU Interface **必须通过系统寄存器访问**，MMIO 方式无效
- PPI 的 interrupt-cell 中 type 字段为 **1**，不是 0
- LPI 的最小对齐要求为 **64KB**，分配内存时必须满足
- 修改中断路由后需确保 **wmb()** 屏障，防止乱序导致丢失
- EOI 必须在 ISR 返回前完成，否则中断永远处于 Active 状态

---

## 9. GIC vs 其他中断控制器对比

| 特性             | ARM GICv3/v4       | x86 APIC/x2APIC    | RISC-V PLIC        | SiFive CLINT       |
| :--------------- | :----------------- | :----------------- | :----------------- | :----------------- |
| 标准化程度       | ARM 官方规范       | Intel/AMD 规范     | RISC-V 特权规范    | SiFive 私有        |
| 最大中断数       | 数万 (LPI)         | 256 (xAPIC) / 2^32 | ~1024              | 极少               |
| 虚拟化支持       | vGIC + Direct LPI  | VT-d / Posted Int  | IMSIC (AIA)        | 无                 |
| 核间中断         | SGI                | IPI via APIC       | Software Interrupt | MSIP               |
| 消息中断         | ITS + LPI          | MSI-X              | IMSIC              | 不支持             |
| 安全隔离         | TrustZone Groups   | TDX/SEV            | PMP/ePMP           | 有限               |

---

## 10. 参考资料

- *ARM Generic Interrupt Controller Architecture Specification* (IHI0069) — GICv3/v4 官方规范
- *ARM System Memory Management Unit Architecture Specification* (IHI0070)
- *Linux Kernel Documentation/devicetree/bindings/interrupt-controller/arm,gic-v3.yaml*
- *Trusted Firmware-A Design Guide* — GIC 初始化流程
- 《ARM System-on-Chip Architecture》— Furber & Seal
- 《Embedded Systems Architecture》— Daniele Lacamera (Chapter on Interrupt Controllers)
- Linaro GICv3/v4 Workshop Slides (公开资料)

---

> 📝 **使用说明**: 本文档覆盖 GIC 从架构原理、硬件组成、软件驱动到调试实践的完整知识体系。适用于嵌入式 Linux 开发、RTOS 移植、虚拟化平台搭建及芯片验证等场景。如需针对特定 SoC（如 RK3588、Jetson Orin、AWS Graviton）补充细节，可在对应章节扩展。