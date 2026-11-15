
#ifndef MMU_H
#define MMU_H

#include <stdint.h>

/* MMU 状态 */
typedef enum
{
    MMU_STATUS_OK = 0,
    MMU_STATUS_ERROR,
    MMU_STATUS_BUSY,
    MMU_STATUS_NOT_FOUND
} MMU_Status;

/* 内存访问权限 */
typedef enum
{
    MMU_PERM_READ  = 1 << 0,
    MMU_PERM_WRITE = 1 << 1,
    MMU_PERM_EXEC  = 1 << 2
} MMU_Permission;

/* 内存属性 */
typedef enum
{
    MMU_MEM_NORMAL = 0,
    MMU_MEM_DEVICE,
    MMU_MEM_UNCACHED
} MMU_MemType;

/* MMU 配置 */
typedef struct
{
    uint32_t page_size;
    uint8_t enable;
} MMU_Config;

/* 地址映射项 */
typedef struct
{
    uint32_t virtual_addr;
    uint32_t physical_addr;
    uint32_t size;

    uint32_t permission;
    MMU_MemType mem_type;

    uint8_t valid;
} MMU_Mapping;

/* 抽象页表 */
#define MMU_MAX_MAPPINGS 32

typedef struct
{
    MMU_Mapping entries[MMU_MAX_MAPPINGS];
    uint32_t count;
} MMU_PageTable;

/* MMU 设备对象 */
typedef struct
{
    MMU_Config config;
    MMU_PageTable *page_table;
    MMU_Status status;
    uint8_t initialized;
} MMU_Device;

/* 驱动接口 */
MMU_Status MMU_Init(MMU_Device *dev,
                    MMU_Config *config,
                    MMU_PageTable *table);

MMU_Status MMU_Map(MMU_Device *dev,
                   uint32_t virtual_addr,
                   uint32_t physical_addr,
                   uint32_t size,
                   uint32_t permission,
                   MMU_MemType type);

MMU_Status MMU_Unmap(MMU_Device *dev,
                     uint32_t virtual_addr);

MMU_Status MMU_Enable(MMU_Device *dev);

MMU_Status MMU_Disable(MMU_Device *dev);

MMU_Status MMU_Translate(MMU_Device *dev,
                         uint32_t virtual_addr,
                         uint32_t *physical_addr);

void MMU_TLB_Invalidate(void);

#endif
