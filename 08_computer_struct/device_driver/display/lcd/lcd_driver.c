#include <stdio.h>
#include <string.h>

#include "lcd_driver.h"

/* LCD 显示缓冲区 */
static uint16_t lcd_buffer[LCD_WIDTH * LCD_HEIGHT];

/* 初始化 LCD */
int LCD_Init(LCD_Device *lcd)
{
    if (lcd == NULL)
        return -1;

    lcd->width = LCD_WIDTH;
    lcd->height = LCD_HEIGHT;

    lcd->color = LCD_COLOR_WHITE;
    lcd->state = LCD_STATE_OFF;

    lcd->framebuffer = lcd_buffer;

    memset(lcd_buffer, 0, sizeof(lcd_buffer));

    printf("[LCD] Initialize LCD\n");
    printf("[LCD] Resolution: %u x %u\n",
           lcd->width, lcd->height);

    return 0;
}

/* 开启 LCD */
int LCD_Enable(LCD_Device *lcd)
{
    if (lcd == NULL)
        return -1;

    lcd->state = LCD_STATE_ON;

    printf("[LCD] Display Enabled\n");

    return 0;
}

/* 关闭 LCD */
int LCD_Disable(LCD_Device *lcd)
{
    if (lcd == NULL)
        return -1;

    lcd->state = LCD_STATE_OFF;

    printf("[LCD] Display Disabled\n");

    return 0;
}

/* 清屏 */
int LCD_Clear(LCD_Device *lcd, uint16_t color)
{
    uint32_t size;

    if (lcd == NULL || lcd->framebuffer == NULL)
        return -1;

    size = (uint32_t)lcd->width * lcd->height;

    for (uint32_t i = 0; i < size; i++) {
        lcd->framebuffer[i] = color;
    }

    printf("[LCD] Clear Screen\n");

    return 0;
}

/* 设置画笔颜色 */
int LCD_SetColor(LCD_Device *lcd, uint16_t color)
{
    if (lcd == NULL)
        return -1;

    lcd->color = color;

    return 0;
}

/* 绘制像素点 */
int LCD_DrawPixel(LCD_Device *lcd,
                  uint16_t x,
                  uint16_t y)
{
    uint32_t index;

    if (lcd == NULL || lcd->framebuffer == NULL)
        return -1;

    if (lcd->state != LCD_STATE_ON)
        return -1;

    if (x >= lcd->width || y >= lcd->height)
        return -1;

    /* 计算像素在 Framebuffer 中的位置 */
    index = (uint32_t)y * lcd->width + x;

    lcd->framebuffer[index] = lcd->color;

    return 0;
}

/* 绘制矩形 */
int LCD_DrawRectangle(LCD_Device *lcd,
                      uint16_t x,
                      uint16_t y,
                      uint16_t width,
                      uint16_t height)
{
    if (lcd == NULL)
        return -1;

    if (width == 0 || height == 0)
        return -1;

    if ((uint32_t)x + width > lcd->width ||
        (uint32_t)y + height > lcd->height)
        return -1;

    for (uint32_t row = y; row < (uint32_t)y + height; row++) {
        for (uint32_t col = x; col < (uint32_t)x + width; col++) {
            LCD_DrawPixel(lcd, (uint16_t)col, (uint16_t)row);
        }
    }

    printf("[LCD] Draw Rectangle\n");

    return 0;
}

/* 刷新显示 */
int LCD_Flush(LCD_Device *lcd)
{
    if (lcd == NULL || lcd->framebuffer == NULL)
        return -1;

    if (lcd->state != LCD_STATE_ON)
        return -1;

    /*
     * 实际硬件中：
     * 将 Framebuffer 数据传输到 LCD 控制器。
     *
     * 可以通过 DMA、RGB Interface、
     * SPI 或 MIPI DSI 等方式传输。
     */

    printf("[LCD] Refresh Display\n");

    return 0;
}

/* 获取 LCD 状态 */
void LCD_GetStatus(LCD_Device *lcd)
{
    if (lcd == NULL)
        return;

    printf("\n========== LCD STATUS ==========\n");

    printf("Resolution : %u x %u\n",
           lcd->width, lcd->height);

    printf("State      : %s\n",
           lcd->state == LCD_STATE_ON ? "ON" : "OFF");

    printf("Color      : 0x%04X\n",
           lcd->color);

    printf("Pixel Format: RGB565\n");

    printf("================================\n");
}

/* 主函数：模拟 LCD 驱动流程 */
int main(void)
{
    LCD_Device lcd;

    /* 1. 初始化 LCD */
    LCD_Init(&lcd);

    /* 2. 开启 LCD */
    LCD_Enable(&lcd);

    /* 3. 清屏为黑色 */
    LCD_Clear(&lcd, LCD_COLOR_BLACK);

    /* 4. 设置画笔颜色为红色 */
    LCD_SetColor(&lcd, LCD_COLOR_RED);

    /* 5. 绘制像素点 */
    LCD_DrawPixel(&lcd, 100, 100);

    /* 6. 设置画笔颜色为绿色 */
    LCD_SetColor(&lcd, LCD_COLOR_GREEN);

    /* 7. 绘制矩形 */
    LCD_DrawRectangle(&lcd, 50, 50, 100, 80);

    /* 8. 刷新显示 */
    LCD_Flush(&lcd);

    /* 9. 获取 LCD 状态 */
    LCD_GetStatus(&lcd);

    /* 10. 关闭 LCD */
    LCD_Disable(&lcd);

    return 0;
}