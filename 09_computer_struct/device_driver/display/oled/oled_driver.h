
#ifndef OLED_DRIVER_H
#define OLED_DRIVER_H

#include <stdint.h>

/* OLED 屏幕参数 */
#define OLED_WIDTH       128
#define OLED_HEIGHT      64
#define OLED_PAGE_NUM    (OLED_HEIGHT / 8)
#define OLED_BUFFER_SIZE (OLED_WIDTH * OLED_PAGE_NUM)

/* OLED 状态 */
typedef enum {
    OLED_STATE_OFF = 0,
    OLED_STATE_ON
} OLED_State;

/* OLED 设备结构体 */
typedef struct {
    uint16_t width;
    uint16_t height;

    OLED_State state;

    /* OLED 显示缓冲区 */
    uint8_t *buffer;

} OLED_Device;

/* OLED 驱动接口 */

/* 初始化 OLED */
int OLED_Init(OLED_Device *oled);

/* 开启 OLED */
int OLED_Enable(OLED_Device *oled);

/* 关闭 OLED */
int OLED_Disable(OLED_Device *oled);

/* 清屏 */
int OLED_Clear(OLED_Device *oled);

/* 设置像素点 */
int OLED_DrawPixel(OLED_Device *oled,
                   uint16_t x,
                   uint16_t y,
                   uint8_t color);

/* 绘制矩形 */
int OLED_DrawRectangle(OLED_Device *oled,
                       uint16_t x,
                       uint16_t y,
                       uint16_t width,
                       uint16_t height,
                       uint8_t color);

/* 刷新显示 */
int OLED_Flush(OLED_Device *oled);

/* 获取 OLED 状态 */
void OLED_GetStatus(OLED_Device *oled);

#endif
