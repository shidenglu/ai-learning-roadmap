
#ifndef MEMORY_HAL_H
#define MEMORY_HAL_H

#include <stdint.h>

/* 硬件初始化 */
int Memory_HAL_Init(void);

/* 硬件读取 */
int Memory_HAL_Read(uint32_t addr,
                    uint8_t *buf,
                    uint32_t len);

/* 硬件写入 */
int Memory_HAL_Write(uint32_t addr,
                     const uint8_t *buf,
                     uint32_t len);

/* 硬件擦除 */
int Memory_HAL_Erase(uint32_t addr,
                     uint32_t len);

/* 硬件关闭 */
int Memory_HAL_DeInit(void);

#endif
