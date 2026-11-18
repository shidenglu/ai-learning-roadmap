#include <stdio.h>
#include "gpio.h"

int main(void)
{
    /* GPIO5配置为输出 */
    gpio_init(5, GPIO_OUTPUT);

    /* GPIO5输出高电平 */
    gpio_set_value(5, GPIO_HIGH);

    printf("GPIO5 HIGH\n");

    /* GPIO3配置为输入 */
    gpio_init(3, GPIO_INPUT);

    if(gpio_get_value(3) == GPIO_HIGH)
    {
        printf("GPIO3 HIGH\n");
    }
    else
    {
        printf("GPIO3 LOW\n");
    }

    return 0;
}