
#include "memory_hal.h"
#include <stdio.h>

int Memory_HAL_Init(void)
{
    printf("[HAL] Memory hardware initialized\n");
    return 0;
}

int Memory_HAL_Read(uint32_t addr,
                    uint8_t *buf,
                    uint32_t len)
{
    if (buf == NULL || len == 0)
        return -1;

    printf("[HAL] Read addr: 0x%08X, len: %u\n",
           addr, len);

    return 0;
}

int Memory_HAL_Write(uint32_t addr,
                     const uint8_t *buf,
                     uint32_t len)
{
    if (buf == NULL || len == 0)
        return -1;

    printf("[HAL] Write addr: 0x%08X, len: %u\n",
           addr, len);

    return 0;
}

int Memory_HAL_Erase(uint32_t addr,
                     uint32_t len)
{
    if (len == 0)
        return -1;

    printf("[HAL] Erase addr: 0x%08X, len: %u\n",
           addr, len);

    return 0;
}

int Memory_HAL_DeInit(void)
{
    printf("[HAL] Memory hardware deinitialized\n");
    return 0;
}
