
#include "mmu.h"
#include "mmu_hal.h"

MMU_Status MMU_Init(MMU_Device *dev,
                    MMU_Config *config,
                    MMU_PageTable *table)
{
    if (dev == NULL || config == NULL || table == NULL)
        return MMU_STATUS_ERROR;

    if (config->page_size == 0)
        return MMU_STATUS_ERROR;

    if (MMU_HAL_Init() != 0)
        return MMU_STATUS_ERROR;

    dev->config = *config;
    dev->page_table = table;
    dev->page_table->count = 0;
    dev->initialized = 1;
    dev->status = MMU_STATUS_OK;

    return MMU_STATUS_OK;
}

/* 建立虚拟地址映射 */
MMU_Status MMU_Map(MMU_Device *dev,
                   uint32_t virtual_addr,
                   uint32_t physical_addr,
                   uint32_t size,
                   uint32_t permission,
                   MMU_MemType type)
{
    MMU_PageTable *table;

    if (dev == NULL || !dev->initialized || size == 0)
        return MMU_STATUS_ERROR;

    table = dev->page_table;

    if (virtual_addr % dev->config.page_size != 0 ||
        physical_addr % dev->config.page_size != 0 ||
        size % dev->config.page_size != 0)
        return MMU_STATUS_ERROR;

    if (table->count >= MMU_MAX_MAPPINGS)
        return MMU_STATUS_ERROR;

    /* 检查虚拟地址区间是否冲突 */
    for (uint32_t i = 0; i < table->count; i++)
    {
        MMU_Mapping *entry = &table->entries[i];

        uint64_t new_end = (uint64_t)virtual_addr + size;
        uint64_t old_end = (uint64_t)entry->virtual_addr
                         + entry->size;

        if (virtual_addr < old_end &&
            entry->virtual_addr < new_end)
            return MMU_STATUS_ERROR;
    }

    MMU_Mapping *entry = &table->entries[table->count++];

    entry->virtual_addr = virtual_addr;
    entry->physical_addr = physical_addr;
    entry->size = size;
    entry->permission = permission;
    entry->mem_type = type;
    entry->valid = 1;

    MMU_HAL_TLB_Invalidate();

    return MMU_STATUS_OK;
}

/* 删除虚拟地址映射 */
MMU_Status MMU_Unmap(MMU_Device *dev,
                     uint32_t virtual_addr)
{
    MMU_PageTable *table;

    if (dev == NULL || !dev->initialized)
        return MMU_STATUS_ERROR;

    table = dev->page_table;

    for (uint32_t i = 0; i < table->count; i++)
    {
        if (table->entries[i].virtual_addr == virtual_addr)
        {
            table->entries[i].valid = 0;

            for (uint32_t j = i; j + 1 < table->count; j++)
                table->entries[j] = table->entries[j + 1];

            table->count--;

            MMU_HAL_TLB_InvalidateAddr(virtual_addr);

            return MMU_STATUS_OK;
        }
    }

    return MMU_STATUS_NOT_FOUND;
}

/* 使能 MMU */
MMU_Status MMU_Enable(MMU_Device *dev)
{
    if (dev == NULL || !dev->initialized)
        return MMU_STATUS_ERROR;

    if (MMU_HAL_SetPageTable((uintptr_t)dev->page_table) != 0)
        return MMU_STATUS_ERROR;

    MMU_HAL_TLB_Invalidate();

    if (MMU_HAL_Enable() != 0)
        return MMU_STATUS_ERROR;

    return MMU_STATUS_OK;
}

/* 关闭 MMU */
MMU_Status MMU_Disable(MMU_Device *dev)
{
    if (dev == NULL || !dev->initialized)
        return MMU_STATUS_ERROR;

    if (MMU_HAL_Disable() != 0)
        return MMU_STATUS_ERROR;

    return MMU_STATUS_OK;
}

/* 模拟地址转换 */
MMU_Status MMU_Translate(MMU_Device *dev,
                         uint32_t virtual_addr,
                         uint32_t *physical_addr)
{
    MMU_PageTable *table;

    if (dev == NULL || !dev->initialized ||
        physical_addr == NULL)
        return MMU_STATUS_ERROR;

    table = dev->page_table;

    for (uint32_t i = 0; i < table->count; i++)
    {
        MMU_Mapping *entry = &table->entries[i];

        uint64_t end = (uint64_t)entry->virtual_addr
                     + entry->size;

        if (entry->valid &&
            virtual_addr >= entry->virtual_addr &&
            virtual_addr < end)
        {
            *physical_addr = entry->physical_addr
                           + (virtual_addr - entry->virtual_addr);

            return MMU_STATUS_OK;
        }
    }

    return MMU_STATUS_NOT_FOUND;
}

/* 刷新 TLB */
void MMU_TLB_Invalidate(void)
{
    MMU_HAL_TLB_Invalidate();
}
