#ifndef LED_DRIVER_H
#define LED_DRIVER_H

#include <stdint.h>

/* LED 状态 */
typedef enum {
    LED_STATE_OFF = 0,
    LED_STATE_ON
} LED_State;

/* LED 设备结构体 */
typedef struct {
    uint32_t led_id;

    LED_State state;

    uint8_t brightness;

    uint8_t gpio_level;

} LED_Device;

/* LED 驱动接口 */

/* 初始化 LED */
int LED_Init(LED_Device *led, uint32_t led_id);

/* 开启 LED */
int LED_On(LED_Device *led);

/* 关闭 LED */
int LED_Off(LED_Device *led);

/* 切换 LED 状态 */
int LED_Toggle(LED_Device *led);

/* LED 闪烁 */
int LED_Blink(LED_Device *led, uint32_t times);

/* 设置 LED 亮度 */
int LED_SetBrightness(LED_Device *led,
                      uint8_t brightness);

/* 获取 LED 状态 */
void LED_GetStatus(LED_Device *led);

#endif