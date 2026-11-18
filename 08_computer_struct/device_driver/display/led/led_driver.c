#include <stdio.h>
#include <stdint.h>

#include "led_driver.h"

/* 初始化 LED */
int LED_Init(LED_Device *led, uint32_t led_id)
{
    if (led == NULL)
        return -1;

    led->led_id = led_id;
    led->state = LED_STATE_OFF;
    led->brightness = 0;
    led->gpio_level = 0;

    printf("[LED] Initialize LED %u\n", led_id);

    return 0;
}

/* 开启 LED */
int LED_On(LED_Device *led)
{
    if (led == NULL)
        return -1;

    led->state = LED_STATE_ON;
    led->gpio_level = 1;

    if (led->brightness == 0)
        led->brightness = 100;

    printf("[LED] LED %u ON\n", led->led_id);

    return 0;
}

/* 关闭 LED */
int LED_Off(LED_Device *led)
{
    if (led == NULL)
        return -1;

    led->state = LED_STATE_OFF;
    led->gpio_level = 0;
    led->brightness = 0;

    printf("[LED] LED %u OFF\n", led->led_id);

    return 0;
}

/* 切换 LED 状态 */
int LED_Toggle(LED_Device *led)
{
    if (led == NULL)
        return -1;

    if (led->state == LED_STATE_ON)
        return LED_Off(led);

    return LED_On(led);
}

/* LED 闪烁 */
int LED_Blink(LED_Device *led, uint32_t times)
{
    if (led == NULL)
        return -1;

    printf("[LED] LED %u Blink %u Times\n",
           led->led_id, times);

    for (uint32_t i = 0; i < times; i++) {
        LED_On(led);
        LED_Off(led);
    }

    return 0;
}

/* 设置 LED 亮度 */
int LED_SetBrightness(LED_Device *led,
                      uint8_t brightness)
{
    if (led == NULL || brightness > 100)
        return -1;

    led->brightness = brightness;

    if (brightness == 0) {
        led->state = LED_STATE_OFF;
        led->gpio_level = 0;
    } else {
        led->state = LED_STATE_ON;
        led->gpio_level = 1;
    }

    /*
     * 实际硬件中：
     * 通过 PWM 控制器配置占空比。
     *
     * 本 Demo 仅模拟 PWM 占空比。
     */

    printf("[LED] Set Brightness: %u%%\n",
           brightness);

    return 0;
}

/* 获取 LED 状态 */
void LED_GetStatus(LED_Device *led)
{
    if (led == NULL)
        return;

    printf("\n========== LED STATUS ==========\n");

    printf("LED ID     : %u\n", led->led_id);

    printf("State      : %s\n",
           led->state == LED_STATE_ON ? "ON" : "OFF");

    printf("GPIO Level : %u\n", led->gpio_level);

    printf("Brightness : %u%%\n", led->brightness);

    printf("================================\n");
}

/* 主函数：模拟 LED 驱动流程 */
int main(void)
{
    LED_Device led;

    /* 1. 初始化 LED */
    LED_Init(&led, 0);

    /* 2. 开启 LED */
    LED_On(&led);

    /* 3. 获取 LED 状态 */
    LED_GetStatus(&led);

    /* 4. 切换 LED 状态 */
    LED_Toggle(&led);

    /* 5. LED 闪烁 */
    LED_Blink(&led, 3);

    /* 6. 设置 LED 亮度 */
    LED_SetBrightness(&led, 50);

    /* 7. 获取 LED 状态 */
    LED_GetStatus(&led);

    /* 8. 关闭 LED */
    LED_Off(&led);

    return 0;
}