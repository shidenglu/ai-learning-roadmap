#include "memory.h"

static int Memory_CheckRange(MemoryDevice *dev,
                             uint32_t addr,
                             uint32_t len)
{
    uint64_t offset;

    if (dev == NULL || len == 0)
        return -1;

    if (addr < dev->config.base_addr)
        return -1;

    offset = (uint64_t)addr - dev->config.base_addr;

    if (offset + len > dev->config.total_size)
        return -1;

    return 0;
}

/* 初始化 */
MemoryStatus Memory_Init(MemoryDevice *dev,
                         const MemoryConfig *config,
                         const MemoryOps *ops)
{
    if (dev == NULL || config == NULL || ops == NULL)
        return MEMORY_STATUS_ERROR;

    if (config->total_size == 0 ||
        ops->init == NULL ||
        ops->read == NULL ||
        ops->write == NULL ||
        ops->deinit == NULL)
        return MEMORY_STATUS_ERROR;

    dev->config = *config;
    dev->ops = *ops;
    dev->initialized = 0;

    if (dev->ops.init() != 0)
        return MEMORY_STATUS_ERROR;

    dev->initialized = 1;
    dev->status = MEMORY_STATUS_OK;

    return MEMORY_STATUS_OK;
}

/* 读取 */
MemoryStatus Memory_Read(MemoryDevice *dev,
                         uint32_t addr,
                         uint8_t *buf,
                         uint32_t len)
{
    if (dev == NULL || !dev->initialized || buf == NULL)
        return MEMORY_STATUS_ERROR;

    if (Memory_CheckRange(dev, addr, len) != 0)
        return MEMORY_STATUS_ERROR;

    if (dev->ops.read(addr, buf, len) != 0)
        return MEMORY_STATUS_ERROR;

    return MEMORY_STATUS_OK;
}

/* 写入 */
MemoryStatus Memory_Write(MemoryDevice *dev,
                          uint32_t addr,
                          const uint8_t *buf,
                          uint32_t len)
{
    if (dev == NULL || !dev->initialized || buf == NULL)
        return MEMORY_STATUS_ERROR;

    if (Memory_CheckRange(dev, addr, len) != 0)
        return MEMORY_STATUS_ERROR;

    if (dev->ops.write(addr, buf, len) != 0)
        return MEMORY_STATUS_ERROR;

    return MEMORY_STATUS_OK;
}

/* 擦除 */
MemoryStatus Memory_Erase(MemoryDevice *dev,
                          uint32_t addr,
                          uint32_t len)
{
    if (dev == NULL || !dev->initialized)
        return MEMORY_STATUS_ERROR;

    if (Memory_CheckRange(dev, addr, len) != 0)
        return MEMORY_STATUS_ERROR;

    if (dev->ops.erase == NULL)
        return MEMORY_STATUS_UNSUPPORTED;

    if (dev->ops.erase(addr, len) != 0)
        return MEMORY_STATUS_ERROR;

    return MEMORY_STATUS_OK;
}

/* 反初始化 */
MemoryStatus Memory_DeInit(MemoryDevice *dev)
{
    if (dev == NULL || !dev->initialized)
        return MEMORY_STATUS_ERROR;

    if (dev->ops.deinit() != 0)
        return MEMORY_STATUS_ERROR;

    dev->initialized = 0;
    dev->status = MEMORY_STATUS_OK;

    return MEMORY_STATUS_OK;
}
