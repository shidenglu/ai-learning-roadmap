#ifndef __GPIO_H__
#define __GPIO_H__

#include <stdint.h>

/* GPIO方向 */
typedef enum
{
    GPIO_INPUT = 0,
    GPIO_OUTPUT
} gpio_dir_t;

/* GPIO电平 */
typedef enum
{
    GPIO_LOW = 0,
    GPIO_HIGH
} gpio_level_t;

/* GPIO初始化 */
void gpio_init(uint32_t pin,
               gpio_dir_t dir);

/* 输出电平 */
void gpio_set_value(uint32_t pin,
                    gpio_level_t value);

/* 读取电平 */
gpio_level_t gpio_get_value(uint32_t pin);

#endif