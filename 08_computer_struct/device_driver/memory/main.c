
#include <stdio.h>
#include "memory.h"
#include "memory_hal.h"

/* HAL 接口适配 */
static int Driver_HW_Init(void)
{
    return Memory_HAL_Init();
}

static int Driver_HW_Read(uint32_t addr,
                          uint8_t *buf,
                          uint32_t len)
{
    return Memory_HAL_Read(addr, buf, len);
}

static int Driver_HW_Write(uint32_t addr,
                           const uint8_t *buf,
                           uint32_t len)
{
    return Memory_HAL_Write(addr, buf, len);
}

static int Driver_HW_Erase(uint32_t addr,
                           uint32_t len)
{
    return Memory_HAL_Erase(addr, len);
}

static int Driver_HW_DeInit(void)
{
    return Memory_HAL_DeInit();
}

int main(void)
{
    MemoryDevice memory;

    MemoryConfig config = {
        .type = MEMORY_TYPE_FLASH,
        .base_addr = 0x1000,
        .total_size = 1024,
        .block_size = 256
    };

    MemoryOps ops = {
        .init = Driver_HW_Init,
        .read = Driver_HW_Read,
        .write = Driver_HW_Write,
        .erase = Driver_HW_Erase,
        .deinit = Driver_HW_DeInit
    };

    uint8_t tx_buf[] = {1, 2, 3, 4};
    uint8_t rx_buf[4];

    /* 初始化 */
    Memory_Init(&memory, &config, &ops);

    /* 写入数据 */
    Memory_Write(&memory, 0x1000,
                 tx_buf, sizeof(tx_buf));

    /* 读取数据 */
    Memory_Read(&memory, 0x1000,
                rx_buf, sizeof(rx_buf));

    /* 擦除数据 */
    Memory_Erase(&memory, 0x1000, 256);

    /* 关闭设备 */
    Memory_DeInit(&memory);

    return 0;
}
