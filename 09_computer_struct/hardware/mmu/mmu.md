# MMU (Memory Management Unit) 技术详解

## 1. 什么是 MMU？

**MMU（内存管理单元）** 是现代处理器（CPU）中的关键硬件组件，主要负责 **虚拟地址到物理地址的转换** 以及 **内存访问权限的控制**。

它是实现现代操作系统核心特性（如虚拟内存、多任务隔离、内存保护）的硬件基础。没有 MMU，就无法运行 Linux、Windows、macOS 等现代通用操作系统。

---

## 2. 核心功能

| 功能         | 描述                                                                 |
| :----------- | :------------------------------------------------------------------- |
| **地址翻译** | 将程序使用的虚拟地址（VA）转换为实际内存的物理地址（PA）             |
| **内存保护** | 检查读写/执行权限，防止进程越界访问或非法操作                        |
| **缓存控制** | 标记内存区域的缓存策略（Cacheable / Non-cacheable / Write-through 等）|
| **TLB 管理** | 维护翻译后备缓冲区，加速地址翻译过程                                 |
| **异常生成** | 当翻译失败或权限违规时，触发 Page Fault 或 Permission Fault          |

---

## 3. 工作原理

### 3.1 地址翻译流程

```text
CPU发出虚拟地址(VA)
        │
        ▼
   ┌─────────┐    Hit     ┌──────────────────────┐
   │   TLB   │ ─────────► │ 直接输出物理地址(PA)   │
   └─────────┘            └──────────────────────┘
        │ Miss
        ▼
   ┌─────────────────┐
   │  Page Table Walk │ ◄── TTBR (Translation Table Base Register)
   │  (页表遍历)      │
   └─────────────────┘
        │
        ▼
   找到页表项(PTE) → 提取物理帧号 + 偏移量 → PA
        │
        ▼
   更新 TLB 缓存

```

### 3.2 多级页表

现代系统普遍采用 **多级页表** 结构以减少内存占用：

- **ARMv8 (AArch64)**: 支持 4KB/16KB/64KB 粒度，通常使用 4 级页表（L0→L1→L2→L3），可寻址 48~52 位虚拟地址空间。
- **x86-64**: 经典 4 级页表（PML4→PDPT→PD→PT），4KB 页面粒度下可寻址 48 位虚拟地址；5 级页表可扩展至 57 位。

> 💡 **为什么用多级页表？**
> 线性页表在 64 位地址空间下需要巨大的连续内存。多级页表允许只分配实际使用的页表节点，大幅减少内存开销。

---

## 4. 关键数据结构与寄存器

### 4.1 页表项 (Page Table Entry, PTE)

每个 PTE 通常包含以下字段：

- **物理帧号 (PFN)**: 对应物理内存页的基地址
- **有效位 (Valid)**: 该页表项是否有效
- **权限位**: Read / Write / Execute / User / Privileged
- **属性位**: Cache policy、Shareability、Access Flag、Dirty Bit
- **NX/XN**: No-Execute 标记，防止代码注入攻击

### 4.2 关键寄存器 (以 ARMv8 为例)

| 寄存器       | 作用                                         |
| :----------- | :------------------------------------------- |
| `TTBR0_EL1`  | 用户空间页表基地址                           |
| `TTBR1_EL1`  | 内核空间页表基地址                           |
| `TCR_EL1`    | 翻译控制寄存器（配置页表粒度、地址宽度等）   |
| `SCTLR_EL1`  | 系统控制寄存器（使能/禁用 MMU）              |
| `ESR_EL1`    | 异常综合征寄存器（记录 fault 原因）          |
| `FAR_EL1`    | 故障地址寄存器（记录触发 fault 的 VA）       |

---

## 5. TLB (Translation Lookaside Buffer)

TLB 是 MMU 内部的 **高速缓存**，用于避免每次内存访问都进行耗时的页表遍历。

- 采用 **全相联 / 组相联** 结构
- 按 **ASID (Address Space Identifier)** 区分不同进程的 TLB 条目
- 上下文切换时需通过 `TLBI` 指令刷新或使用 ASID 避免全局刷新
- 典型命中率 > 99%，Miss 代价可达数十到数百个时钟周期

---

## 6. MMU 与操作系统的协作

```text
┌─────────────────────────────────────────┐
│           应用程序 (User Space)          │
├─────────────────────────────────────────┤
│         系统调用 / Page Fault           │
├─────────────────────────────────────────┤
│          OS 内核 (Kernel Space)         │
│  • 创建/销毁页表                        │
│  • 处理 Page Fault (缺页中断)            │
│  • 内存映射 (mmap)                      │
│  • COW (Copy-on-Write)                  │
│  • 交换 (Swap In/Out)                   │
├─────────────────────────────────────────┤
│              MMU 硬件                   │
│  • 自动地址翻译                         │
│  • 权限检查                             │
│  • 触发异常通知 OS                       │
└─────────────────────────────────────────┘

```

### 典型交互场景

1.  **缺页异常 (Page Fault)**: MMU 发现 PTE 无效 → 触发异常 → OS 分配物理页并更新页表 → 重试指令
2.  **COW (Copy-on-Write)**: 父子进程共享只读页 → 子进程写入 → MMU 触发写保护异常 → OS 复制页面并更新子进程页表为可写
3.  **Swap**: 物理内存不足 → OS 将页换出到磁盘 → 清除 PTE 有效位 → 下次访问触发 Page Fault → 换入

---

## 7. 常见架构对比

| 特性           | ARMv8 (AArch64)     | x86-64            | RISC-V (Sv39/Sv48) |
| :------------- | :------------------ | :---------------- | :----------------- |
| 页表级数       | 4级 (4KB粒度)       | 4级/5级           | 3级(Sv39)/4级(Sv48)|
| ASID 支持      | ✅ (8/16 bit)       | ❌ (需 PCID)      | ✅                 |
| 大小页混合     | ✅ (4K/16K/64K)     | ✅ (4K/2M/1G)     | ✅ (4K/2M/1G)      |
| 安全扩展       | TrustZone / EL2/EL3 | SMM / SGX         | PMP / ePMP         |
| 典型应用       | 移动/IoT/服务器     | PC/服务器/云      | 嵌入式/新兴SoC     |

---

## 8. 调试与常见问题

### 常见 Fault 类型

- **Translation Fault**: 页表项无效，页表路径不完整
- **Permission Fault**: 权限不匹配（如用户态访问内核页、写入只读页）
- **Alignment Fault**: 非对齐访问（某些架构严格要求对齐）
- **External Abort**: 物理内存不可达或总线错误

### 调试技巧

1.  读取 `ESR_EL1` / `FAR_EL1` 确定 fault 类型和地址
2.  使用 `ptdump` / `/sys/kernel/debug/page_tables` 导出页表内容
3.  利用 QEMU/GDB 的 `monitor info mem` 查看虚拟到物理映射
4.  检查 `TTBR` 和 `TCR` 配置是否与预期一致
5.  确认 TLB 是否在页表修改后正确 invalidate

---

## 9. 参考资料

- *ARM Architecture Reference Manual for A-profile* (DDI0487)
- *Intel® 64 and IA-32 Architectures Software Developer's Manual* Vol.3
- *RISC-V Privileged Specification*
- 《Operating Systems: Three Easy Pieces》- Memory Virtualization 章节
- 《Understanding the Linux Virtual Memory Manager》- Mel Gorman

---

> 📝 **使用说明**: 本文档涵盖 MMU 的核心概念、工作原理及跨架构对比。如需针对特定架构深入展开，可在此基础上补充对应章节细节。