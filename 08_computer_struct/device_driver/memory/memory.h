
#ifndef MEMORY_H
#define MEMORY_H

#include <stdint.h>

/* 内存设备类型 */
typedef enum
{
    MEMORY_TYPE_RAM = 0,
    MEMORY_TYPE_FLASH,
    MEMORY_TYPE_UNKNOWN
} MemoryType;

/* 内存设备状态 */
typedef enum
{
    MEMORY_STATUS_OK = 0,
    MEMORY_STATUS_ERROR,
    MEMORY_STATUS_BUSY,
    MEMORY_STATUS_TIMEOUT,
    MEMORY_STATUS_UNSUPPORTED
} MemoryStatus;

/* 内存设备配置 */
typedef struct
{
    MemoryType type;
    uint32_t base_addr;
    uint32_t total_size;
    uint32_t block_size;
} MemoryConfig;

/* 底层硬件操作接口 */
typedef struct
{
    int (*init)(void);
    int (*read)(uint32_t addr, uint8_t *buf, uint32_t len);
    int (*write)(uint32_t addr, const uint8_t *buf, uint32_t len);
    int (*erase)(uint32_t addr, uint32_t len);
    int (*deinit)(void);
} MemoryOps;

/* 内存设备对象 */
typedef struct
{
    MemoryConfig config;
    MemoryOps ops;

    MemoryStatus status;
    uint8_t initialized;
} MemoryDevice;

/* 驱动接口 */
MemoryStatus Memory_Init(MemoryDevice *dev,
                         const MemoryConfig *config,
                         const MemoryOps *ops);

MemoryStatus Memory_Read(MemoryDevice *dev,
                         uint32_t addr,
                         uint8_t *buf,
                         uint32_t len);

MemoryStatus Memory_Write(MemoryDevice *dev,
                          uint32_t addr,
                          const uint8_t *buf,
                          uint32_t len);

MemoryStatus Memory_Erase(MemoryDevice *dev,
                          uint32_t addr,
                          uint32_t len);

MemoryStatus Memory_DeInit(MemoryDevice *dev);

#endif
