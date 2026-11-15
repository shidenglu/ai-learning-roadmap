
#include <stdio.h>
#include "mmu_hal.h"

int MMU_HAL_Init(void)
{
    printf("[HAL] MMU hardware initialized\n");
    return 0;
}

int MMU_HAL_SetPageTable(uintptr_t addr)
{
    printf("[HAL] Page table base: 0x%llX\n",
           (unsigned long long)addr);

    return 0;
}

int MMU_HAL_Enable(void)
{
    printf("[HAL] MMU enabled\n");
    return 0;
}

int MMU_HAL_Disable(void)
{
    printf("[HAL] MMU disabled\n");
    return 0;
}

void MMU_HAL_TLB_Invalidate(void)
{
    printf("[HAL] TLB invalidated\n");
}

void MMU_HAL_TLB_InvalidateAddr(uint32_t addr)
{
    printf("[HAL] TLB invalidate address: 0x%08X\n",
           addr);
}
