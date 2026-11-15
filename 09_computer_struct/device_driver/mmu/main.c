
#include <stdio.h>
#include "mmu.h"

int main(void)
{
    MMU_Device mmu;

    MMU_PageTable page_table;

    MMU_Config config = {
        .page_size = 4096,
        .enable = 1
    };

    uint32_t physical_addr;

    /* 初始化 MMU */
    MMU_Init(&mmu, &config, &page_table);

    /* 建立地址映射 */
    MMU_Map(&mmu,
            0x10000000,
            0x80000000,
            0x2000,
            MMU_PERM_READ | MMU_PERM_WRITE,
            MMU_MEM_NORMAL);

    /* 开启 MMU */
    MMU_Enable(&mmu);

    /* 虚拟地址转换 */
    if (MMU_Translate(&mmu,
                      0x10000100,
                      &physical_addr) == MMU_STATUS_OK)
    {
        printf("Virtual Address: 0x10000100\n");
        printf("Physical Address: 0x%08X\n",
               physical_addr);
    }

    /* 删除映射 */
    MMU_Unmap(&mmu, 0x10000000);

    /* 关闭 MMU */
    MMU_Disable(&mmu);

    return 0;
}
