#include "gpio.h"

/*
 * 模拟GPIO寄存器
 */

static volatile uint32_t GPIO_DIR_REG;
static volatile uint32_t GPIO_OUT_REG;
static volatile uint32_t GPIO_IN_REG;

/*
 * GPIO初始化
 */
void gpio_init(uint32_t pin,
               gpio_dir_t dir)
{
    if(dir == GPIO_OUTPUT)
    {
        GPIO_DIR_REG |= (1 << pin);
    }
    else
    {
        GPIO_DIR_REG &= ~(1 << pin);
    }
}

/*
 * GPIO输出
 */
void gpio_set_value(uint32_t pin,
                    gpio_level_t value)
{
    if(value == GPIO_HIGH)
    {
        GPIO_OUT_REG |= (1 << pin);
    }
    else
    {
        GPIO_OUT_REG &= ~(1 << pin);
    }
}

/*
 * GPIO输入
 */
gpio_level_t gpio_get_value(uint32_t pin)
{
    if(GPIO_IN_REG & (1 << pin))
    {
        return GPIO_HIGH;
    }

    return GPIO_LOW;
}