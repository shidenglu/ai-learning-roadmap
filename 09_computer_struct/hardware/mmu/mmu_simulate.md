# MMU 地址转换 C 语言模拟实现

## 1. 概述

本程序使用纯 C 语言模拟了 MMU 的核心工作流程。为了便于理解，我们采用了一套简化的地址空间参数：

-   **虚拟地址宽度**: 16-bit (寻址空间 64KB)
-   **页面大小**: 256 Bytes (8-bit 偏移量)
-   **页表结构**: 两级页表 (Level-1 + Level-2)
-   **索引位数**: L1 Index = 4bit, L2 Index = 4bit, Offset = 8bit

> 💡 **设计目的**：真实系统（如 ARMv8/x86_64）的地址位宽为 39~48 位，直接模拟会导致代码极其复杂。本示例保留了多级页表、TLB、权限检查等所有核心逻辑，仅缩小了数值规模以便于单步调试和理解。

## 2. 完整 C 代码

将以下内容保存为 `mmu_sim.c`：

```c
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

/*=============================================================
 * 1. MMU 参数定义 (简化模型)
 *============================================================*/
#define VA_BITS         16      // 虚拟地址总宽度
#define PAGE_SIZE       256     // 页面大小 (Bytes)
#define OFFSET_BITS     8       // log2(PAGE_SIZE)
#define L2_INDEX_BITS   4       // 二级页表索引位数
#define L1_INDEX_BITS   4       // 一级页表索引位数

#define NUM_L1_ENTRIES  (1 << L1_INDEX_BITS)   // 16
#define NUM_L2_ENTRIES  (1 << L2_INDEX_BITS)   // 16
#define TLB_SIZE        4                       // TLB 条目数

// 页表项标志位
#define PTE_VALID       0x01    // 有效位
#define PTE_READ        0x02    // 可读
#define PTE_WRITE       0x04    // 可写
#define PTE_EXEC        0x08    // 可执行

/*=============================================================
 * 2. 数据结构定义
 *============================================================*/

// 页表项 (Page Table Entry)
typedef struct {
    uint16_t pfn;       // 物理帧号 (Physical Frame Number)
    uint8_t  flags;     // 权限与属性标志
} PTE;

// TLB 条目
typedef struct {
    bool     valid;
    uint16_t vpn;       // 虚拟页号 (作为 Tag)
    uint16_t pfn;       // 物理帧号
    uint8_t  flags;     // 缓存的权限信息
} TLBEntry;

// MMU 模拟器上下文
typedef struct {
    PTE      l1_table[NUM_L1_ENTRIES];              // 一级页表
    PTE      l2_tables[NUM_L1_ENTRIES][NUM_L2_ENTRIES]; // 二级页表池
    TLBEntry tlb[TLB_SIZE];                          // TLB 缓存
    uint32_t stats_tlb_hit;                         // 统计: TLB 命中
    uint32_t stats_tlb_miss;                        // 统计: TLB Miss
} MMU;

/*=============================================================
 * 3. 辅助函数
 *============================================================*/

// 从虚拟地址中提取各字段
static inline uint8_t get_l1_index(uint16_t va) {
    return (va >> (OFFSET_BITS + L2_INDEX_BITS)) & ((1 << L1_INDEX_BITS) - 1);
}

static inline uint8_t get_l2_index(uint16_t va) {
    return (va >> OFFSET_BITS) & ((1 << L2_INDEX_BITS) - 1);
}

static inline uint8_t get_offset(uint16_t va) {
    return va & ((1 << OFFSET_BITS) - 1);
}

static inline uint16_t get_vpn(uint16_t va) {
    return va >> OFFSET_BITS;
}

// 初始化 MMU
void mmu_init(MMU *mmu) {
    memset(mmu, 0, sizeof(MMU));
    printf("[MMU] Initialized: VA=%d-bit, Page=%dB, L1=%d, L2=%d, TLB=%d\n",
           VA_BITS, PAGE_SIZE, NUM_L1_ENTRIES, NUM_L2_ENTRIES, TLB_SIZE);
}

// 建立映射: VA -> PA
bool mmu_map(MMU *mmu, uint16_t va, uint16_t pa, uint8_t flags) {
    uint8_t l1_idx = get_l1_index(va);
    uint8_t l2_idx = get_l2_index(va);
    uint16_t pfn = pa >> OFFSET_BITS;

    // 标记 L1 表项有效 (指向对应的 L2 表)
    mmu->l1_table[l1_idx].flags |= PTE_VALID;

    // 填写 L2 表项
    mmu->l2_tables[l1_idx][l2_idx].pfn = pfn;
    mmu->l2_tables[l1_idx][l2_idx].flags = flags | PTE_VALID;

    printf("[MAP] VA=0x%04X -> PA=0x%04X (L1[%d].L2[%d], flags=0x%02X)\n",
           va, pa, l1_idx, l2_idx, flags);
    return true;
}

/*=============================================================
 * 4. 核心: TLB 查找
 *============================================================*/
static bool tlb_lookup(MMU *mmu, uint16_t vpn, uint16_t *pfn_out, uint8_t *flags_out) {
    for (int i = 0; i < TLB_SIZE; i++) {
        if (mmu->tlb[i].valid && mmu->tlb[i].vpn == vpn) {
            *pfn_out = mmu->tlb[i].pfn;
            *flags_out = mmu->tlb[i].flags;
            mmu->stats_tlb_hit++;
            printf("  [TLB] HIT at entry %d (VPN=0x%03X -> PFN=0x%03X)\n",
                   i, vpn, *pfn_out);
            return true;
        }
    }
    mmu->stats_tlb_miss++;
    printf("  [TLB] MISS (VPN=0x%03X)\n", vpn);
    return false;
}

// 简单替换策略: 替换第一个无效条目，否则替换 entry[0] (FIFO简化版)
static void tlb_insert(MMU *mmu, uint16_t vpn, uint16_t pfn, uint8_t flags) {
    int slot = 0;
    for (int i = 0; i < TLB_SIZE; i++) {
        if (!mmu->tlb[i].valid) { slot = i; break; }
    }
    mmu->tlb[slot].valid = true;
    mmu->tlb[slot].vpn = vpn;
    mmu->tlb[slot].pfn = pfn;
    mmu->tlb[slot].flags = flags;
    printf("  [TLB] INSERT at entry %d\n", slot);
}

/*=============================================================
 * 5. 核心: MMU 地址翻译
 *============================================================*/
typedef enum {
    TRANSLATE_OK = 0,
    TRANSLATE_FAULT_L1,     // L1 页表项无效
    TRANSLATE_FAULT_L2,     // L2 页表项无效
    TRANSLATE_PERM_READ,    // 读权限违规
    TRANSLATE_PERM_WRITE,   // 写权限违规
    TRANSLATE_PERM_EXEC,    // 执行权限违规
} TranslateResult;

TranslateResult mmu_translate(MMU *mmu, uint16_t va, uint16_t *pa_out,
                              bool is_write, bool is_exec) {
    uint16_t vpn = get_vpn(va);
    uint8_t offset = get_offset(va);
    uint16_t pfn;
    uint8_t flags;

    printf("\n[TRANSLATE] VA=0x%04X (L1=%d, L2=%d, Off=%d) %s%s\n",
           va, get_l1_index(va), get_l2_index(va), offset,
           is_write ? "[W]" : "[R]", is_exec ? "[X]" : "");

    // Step 1: 查 TLB
    if (tlb_lookup(mmu, vpn, &pfn, &flags)) {
        goto permission_check;
    }

    // Step 2: TLB Miss → Page Table Walk
    printf("  [WALK] Starting page table walk...\n");

    uint8_t l1_idx = get_l1_index(va);
    if (!(mmu->l1_table[l1_idx].flags & PTE_VALID)) {
        printf("  [FAULT] L1 entry invalid at index %d\n", l1_idx);
        return TRANSLATE_FAULT_L1;
    }

    uint8_t l2_idx = get_l2_index(va);
    PTE *l2_pte = &mmu->l2_tables[l1_idx][l2_idx];
    if (!(l2_pte->flags & PTE_VALID)) {
        printf("  [FAULT] L2 entry invalid at L1[%d].L2[%d]\n", l1_idx, l2_idx);
        return TRANSLATE_FAULT_L2;
    }

    pfn = l2_pte->pfn;
    flags = l2_pte->flags;
    printf("  [WALK] Found PTE: PFN=0x%03X, flags=0x%02X\n", pfn, flags);

    // Step 3: 填充 TLB
    tlb_insert(mmu, vpn, pfn, flags);

permission_check:
    // Step 4: 权限检查
    if (is_write && !(flags & PTE_WRITE)) {
        printf("  [FAULT] Write permission denied (flags=0x%02X)\n", flags);
        return TRANSLATE_PERM_WRITE;
    }
    if (is_exec && !(flags & PTE_EXEC)) {
        printf("  [FAULT] Execute permission denied (flags=0x%02X)\n", flags);
        return TRANSLATE_PERM_EXEC;
    }
    if (!is_write && !is_exec && !(flags & PTE_READ)) {
        printf("  [FAULT] Read permission denied (flags=0x%02X)\n", flags);
        return TRANSLATE_PERM_READ;
    }

    // Step 5: 合成物理地址
    *pa_out = (pfn << OFFSET_BITS) | offset;
    printf("  [OK] PA=0x%04X (PFN=0x%03X | Offset=0x%02X)\n", *pa_out, pfn, offset);
    return TRANSLATE_OK;
}

/*=============================================================
 * 6. 测试主程序
 *============================================================*/
const char* result_str(TranslateResult r) {
    switch(r) {
        case TRANSLATE_OK:          return "SUCCESS";
        case TRANSLATE_FAULT_L1:    return "L1 FAULT";
        case TRANSLATE_FAULT_L2:    return "L2 FAULT";
        case TRANSLATE_PERM_READ:   return "READ PERM FAULT";
        case TRANSLATE_PERM_WRITE:  return "WRITE PERM FAULT";
        case TRANSLATE_PERM_EXEC:   return "EXEC PERM FAULT";
        default:                    return "UNKNOWN";
    }
}

int main(void) {
    MMU mmu;
    mmu_init(&mmu);

    printf("\n===== Phase 1: 建立页表映射 =====\n");
    // 映射: VA 0x1234 -> PA 0xAB34 (读写)
    mmu_map(&mmu, 0x1234, 0xAB34, PTE_READ | PTE_WRITE);
    // 映射: VA 0x2300 -> PA 0xCD00 (只读+可执行, 代码段)
    mmu_map(&mmu, 0x2300, 0xCD00, PTE_READ | PTE_EXEC);
    // 映射: VA 0x3400 -> PA 0xEF00 (只读数据)
    mmu_map(&mmu, 0x3400, 0xEF00, PTE_READ);

    uint16_t pa;
    TranslateResult res;

    printf("\n===== Phase 2: 正常翻译测试 =====\n");

    // Test 1: 首次访问 (TLB Miss + Page Walk)
    res = mmu_translate(&mmu, 0x1234, &pa, false, false);
    printf("  >> Result: %s\n\n", result_str(res));

    // Test 2: 再次访问同一地址 (TLB Hit)
    res = mmu_translate(&mmu, 0x1234, &pa, false, false);
    printf("  >> Result: %s\n\n", result_str(res));

    // Test 3: 同页不同偏移 (TLB Hit, 因为 VPN 相同)
    res = mmu_translate(&mmu, 0x12FF, &pa, true, false);
    printf("  >> Result: %s\n\n", result_str(res));

    printf("\n===== Phase 3: 异常与权限测试 =====\n");

    // Test 4: 未映射地址 (L2 Fault)
    res = mmu_translate(&mmu, 0x4500, &pa, false, false);
    printf("  >> Result: %s\n\n", result_str(res));

    // Test 5: 写入只读页面 (Write Permission Fault)
    res = mmu_translate(&mmu, 0x3400, &pa, true, false);
    printf("  >> Result: %s\n\n", result_str(res));

    // Test 6: 执行非可执行页面 (Exec Permission Fault)
    res = mmu_translate(&mmu, 0x1234, &pa, false, true);
    printf("  >> Result: %s\n\n", result_str(res));

    // Test 7: 读取代码段 (应成功)
    res = mmu_translate(&mmu, 0x2300, &pa, false, false);
    printf("  >> Result: %s\n\n", result_str(res));

    printf("\n===== Statistics =====\n");
    printf("TLB Hits:   %u\n", mmu.stats_tlb_hit);
    printf("TLB Misses: %u\n", mmu.stats_tlb_miss);
    printf("Hit Rate:   %.1f%%\n",
           mmu.stats_tlb_hit * 100.0 / (mmu.stats_tlb_hit + mmu.stats_tlb_miss));

    return 0;
}

```

## 3. 编译与运行

```bash
gcc -Wall -Wextra -std=c11 -o mmu_sim mmu_sim.c
./mmu_sim

```

### 预期输出片段

```text
[TRANSLATE] VA=0x1234 (L1=1, L2=2, Off=52) [R]
  [TLB] MISS (VPN=0x012)
  [WALK] Starting page table walk...
  [WALK] Found PTE: PFN=0x0AB, flags=0x03
  [TLB] INSERT at entry 0
  [OK] PA=0xAB34 (PFN=0x0AB | Offset=0x34)
  >> Result: SUCCESS

[TRANSLATE] VA=0x1234 (L1=1, L2=2, Off=52) [R]
  [TLB] HIT at entry 0 (VPN=0x012 -> PFN=0x0AB)
  [OK] PA=0xAB34 (PFN=0x0AB | Offset=0x34)
  >> Result: SUCCESS

[TRANSLATE] VA=0x3400 (L1=3, L2=4, Off=0) [W]
  [TLB] MISS (VPN=0x034)
  [WALK] Starting page table walk...
  [WALK] Found PTE: PFN=0x0EF, flags=0x03
  [TLB] INSERT at entry 2
  [FAULT] Write permission denied (flags=0x03)
  >> Result: WRITE PERM FAULT

```

## 4. 代码架构解析

### 4.1 地址拆分示意

以 `VA = 0x1234` 为例（16-bit 地址，256B 页面）：

```text
VA = 0x1234 = 0001 0010 0011 0100
              ├─┤ ├─┤ ├──────┤
              │   │   └── Offset (8 bit) = 0x34
              │   └────── L2 Index (4 bit) = 0x2
              └────────── L1 Index (4 bit) = 0x1

```

### 4.2 翻译流程对应关系

| 真实 MMU 硬件行为               | 本程序模拟函数              |
| :------------------------------ | :-------------------------- |
| CPU 发出虚拟地址                | `mmu_translate(va, ...)`    |
| TLB 并行查找                    | `tlb_lookup()`              |
| TLB Miss → Hardware Page Walk   | L1/L2 数组逐级索引          |
| 权限检查电路                    | `permission_check` 标签段   |
| TLB Fill                        | `tlb_insert()`              |
| 合成物理地址输出                | `(pfn << OFFSET) \| offset` |
| Fault 信号 → Exception          | 返回 `TranslateResult` 枚举 |

### 4.3 可扩展方向

如需进一步扩展此模拟器，建议按以下优先级进行：

1.  **增加 ASID 支持**: 在 TLB 条目中加入 ASID 字段，模拟进程切换时不需 flush TLB
2.  **实现多级 TLB**: 添加 L1-TLB (小/快) + L2-TLB (大/慢) 层次结构
3.  **增加 Dirty/Access Bit**: 模拟硬件自动设置 Access Flag 和 Dirty Bit
4.  **对接内存模拟器**: 用 malloc 分配物理内存数组，实现真正的读写操作
5.  **增大地址空间**: 改为 32-bit 或 64-bit 模型，使用动态分配的页表节点代替静态数组

## 5. 注意事项

-   本程序是 **功能级模拟**，非周期精确模拟，不包含流水线、乱序、总线延迟等微架构细节
-   TLB 替换策略使用了极简 FIFO，真实硬件通常使用 LRU 或伪 LRU
-   页表存储在程序内存中，不代表真实物理内存布局
-   此模型适合操作系统课程实验、嵌入式裸机开发学习及面试准备使用