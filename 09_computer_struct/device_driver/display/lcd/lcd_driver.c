#ifndef LCD_DRIVER_H
#define LCD_DRIVER_H

#include <stdint.h>

/* LCD 屏幕参数 */
#define LCD_WIDTH       320
#define LCD_HEIGHT      240

/* RGB565 颜色格式 */
#define LCD_COLOR_BLACK     0x0000
#define LCD_COLOR_WHITE     0xFFFF
#define LCD_COLOR_RED       0xF800
#define LCD_COLOR_GREEN     0x07E0
#define LCD_COLOR_BLUE      0x001F

/* LCD 状态 */
typedef enum {
    LCD_STATE_OFF = 0,
    LCD_STATE_ON
} LCD_State;

/* LCD 设备结构体 */
typedef struct {
    uint16_t width;
    uint16_t height;

    uint16_t color;

    LCD_State state;

    /* Framebuffer */
    uint16_t *framebuffer;

} LCD_Device;

/* LCD 驱动接口 */

/* 初始化 LCD */
int LCD_Init(LCD_Device *lcd);

/* 开启 LCD */
int LCD_Enable(LCD_Device *lcd);

/* 关闭 LCD */
int LCD_Disable(LCD_Device *lcd);

/* 清屏 */
int LCD_Clear(LCD_Device *lcd, uint16_t color);

/* 设置画笔颜色 */
int LCD_SetColor(LCD_Device *lcd, uint16_t color);

/* 绘制像素点 */
int LCD_DrawPixel(LCD_Device *lcd,
                  uint16_t x,
                  uint16_t y);

/* 绘制矩形 */
int LCD_DrawRectangle(LCD_Device *lcd,
                      uint16_t x,
                      uint16_t y,
                      uint16_t width,
                      uint16_t height);

/* 刷新显示 */
int LCD_Flush(LCD_Device *lcd);

/* 获取 LCD 状态 */
void LCD_GetStatus(LCD_Device *lcd);

#endif