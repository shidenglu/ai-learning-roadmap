
#ifndef MMU_HAL_H
#define MMU_HAL_H

#include <stdint.h>

/* 初始化 MMU 硬件 */
int MMU_HAL_Init(void);

/* 设置页表基地址 */
int MMU_HAL_SetPageTable(uintptr_t addr);

/* 使能 MMU */
int MMU_HAL_Enable(void);

/* 关闭 MMU */
int MMU_HAL_Disable(void);

/* 刷新 TLB */
void MMU_HAL_TLB_Invalidate(void);

/* 刷新指定虚拟地址的 TLB */
void MMU_HAL_TLB_InvalidateAddr(uint32_t addr);

#endif
