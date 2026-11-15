#include <stdio.h>
#include <string.h>

#include "oled_driver.h"

/* OLED 显示缓冲区 */
static uint8_t oled_buffer[OLED_BUFFER_SIZE];

/*
 * 模拟 I2C 命令传输
 *
 * 真实硬件中需要调用 I2C 驱动接口。
 */
static int OLED_WriteCommand(uint8_t command)
{
    (void)command;

    return 0;
}

/*
 * 模拟 I2C 数据传输
 *
 * 真实硬件中需要将数据发送到 SSD1306。
 */
static int OLED_WriteData(const uint8_t *data, uint16_t length)
{
    if (data == NULL || length == 0)
        return -1;

    return 0;
}

/* 初始化 OLED */
int OLED_Init(OLED_Device *oled)
{
    if (oled == NULL)
        return -1;

    oled->width = OLED_WIDTH;
    oled->height = OLED_HEIGHT;
    oled->state = OLED_STATE_OFF;
    oled->buffer = oled_buffer;

    memset(oled_buffer, 0, sizeof(oled_buffer));

    printf("[OLED] Initialize SSD1306\n");

    /* 发送 SSD1306 初始化命令 */
    OLED_WriteCommand(0xAE); /* Display OFF */
    OLED_WriteCommand(0xD5); /* Display Clock */
    OLED_WriteCommand(0x80);
    OLED_WriteCommand(0xA8); /* Multiplex Ratio */
    OLED_WriteCommand(0x3F);
    OLED_WriteCommand(0xD3); /* Display Offset */
    OLED_WriteCommand(0x00);
    OLED_WriteCommand(0x40); /* Start Line */
    OLED_WriteCommand(0x8D); /* Charge Pump */
    OLED_WriteCommand(0x14);
    OLED_WriteCommand(0x20); /* Memory Addressing Mode */
    OLED_WriteCommand(0x02); /* Page Addressing Mode */
    OLED_WriteCommand(0xA1); /* Segment Remap */
    OLED_WriteCommand(0xC8); /* COM Scan Direction */
    OLED_WriteCommand(0xDA); /* COM Pins */
    OLED_WriteCommand(0x12);
    OLED_WriteCommand(0x81); /* Contrast */
    OLED_WriteCommand(0x7F);
    OLED_WriteCommand(0xD9); /* Pre-charge Period */
    OLED_WriteCommand(0xF1);
    OLED_WriteCommand(0xDB); /* VCOMH */
    OLED_WriteCommand(0x40);
    OLED_WriteCommand(0xA4); /* Display RAM */
    OLED_WriteCommand(0xA6); /* Normal Display */

    printf("[OLED] Resolution: %u x %u\n",
           oled->width, oled->height);

    return 0;
}

/* 开启 OLED */
int OLED_Enable(OLED_Device *oled)
{
    if (oled == NULL)
        return -1;

    if (OLED_WriteCommand(0xAF) != 0)
        return -1;

    oled->state = OLED_STATE_ON;

    printf("[OLED] Display Enabled\n");

    return 0;
}

/* 关闭 OLED */
int OLED_Disable(OLED_Device *oled)
{
    if (oled == NULL)
        return -1;

    if (OLED_WriteCommand(0xAE) != 0)
        return -1;

    oled->state = OLED_STATE_OFF;

    printf("[OLED] Display Disabled\n");

    return 0;
}

/* 清屏 */
int OLED_Clear(OLED_Device *oled)
{
    if (oled == NULL || oled->buffer == NULL)
        return -1;

    memset(oled->buffer, 0, OLED_BUFFER_SIZE);

    printf("[OLED] Clear Screen\n");

    return 0;
}

/* 绘制像素点 */
int OLED_DrawPixel(OLED_Device *oled,
                   uint16_t x,
                   uint16_t y,
                   uint8_t color)
{
    uint32_t index;
    uint8_t bit;

    if (oled == NULL || oled->buffer == NULL)
        return -1;

    if (x >= oled->width || y >= oled->height)
        return -1;

    /* 计算缓冲区索引 */
    index = x + (y / 8) * oled->width;

    /* 计算像素所在 bit */
    bit = y % 8;

    if (color) {
        oled->buffer[index] |= (1U << bit);
    } else {
        oled->buffer[index] &= ~(1U << bit);
    }

    return 0;
}

/* 绘制矩形 */
int OLED_DrawRectangle(OLED_Device *oled,
                       uint16_t x,
                       uint16_t y,
                       uint16_t width,
                       uint16_t height,
                       uint8_t color)
{
    if (oled == NULL)
        return -1;

    if (width == 0 || height == 0)
        return -1;

    if ((uint32_t)x + width > oled->width ||
        (uint32_t)y + height > oled->height)
        return -1;

    for (uint32_t row = y; row < (uint32_t)y + height; row++) {
        for (uint32_t col = x; col < (uint32_t)x + width; col++) {
            if (OLED_DrawPixel(oled,
                               (uint16_t)col,
                               (uint16_t)row,
                               color) != 0) {
                return -1;
            }
        }
    }

    printf("[OLED] Draw Rectangle\n");

    return 0;
}

/* 刷新 OLED */
int OLED_Flush(OLED_Device *oled)
{
    if (oled == NULL || oled->buffer == NULL)
        return -1;

    if (oled->state != OLED_STATE_ON)
        return -1;

    /*
     * 按 Page 逐页传输显示数据
     */
    for (uint8_t page = 0; page < OLED_PAGE_NUM; page++) {

        /* 设置当前 Page */
        if (OLED_WriteCommand(0xB0 | page) != 0)
            return -1;

        /* 设置列地址起始位置 */
        if (OLED_WriteCommand(0x00) != 0)
            return -1;

        if (OLED_WriteCommand(0x10) != 0)
            return -1;

        /* 计算当前 Page 的缓冲区位置 */
        uint16_t offset = page * OLED_WIDTH;

        /* 发送当前 Page 的数据 */
        if (OLED_WriteData(&oled->buffer[offset],
                           OLED_WIDTH) != 0) {
            return -1;
        }
    }

    printf("[OLED] Refresh Display\n");

    return 0;
}

/* 获取 OLED 状态 */
void OLED_GetStatus(OLED_Device *oled)
{
    if (oled == NULL)
        return;

    printf("\n========== OLED STATUS ==========\n");

    printf("Resolution : %u x %u\n",
           oled->width, oled->height);

    printf("State      : %s\n",
           oled->state == OLED_STATE_ON ? "ON" : "OFF");

    printf("Pixel      : Monochrome\n");

    printf("Controller : SSD1306\n");

    printf("Interface  : I2C (Simulated)\n");

    printf("Buffer Size: %u Bytes\n",
           OLED_BUFFER_SIZE);

    printf("=================================\n");
}

/* 主函数：模拟 OLED 驱动流程 */
int main(void)
{
    OLED_Device oled;

    /* 1. 初始化 OLED */
    OLED_Init(&oled);

    /* 2. 开启 OLED */
    OLED_Enable(&oled);

    /* 3. 清屏 */
    OLED_Clear(&oled);

    /* 4. 绘制像素点 */
    OLED_DrawPixel(&oled, 20, 20, 1);

    /* 5. 绘制矩形 */
    OLED_DrawRectangle(&oled,
                       30, 20,
                       50, 30,
                       1);

    /* 6. 刷新显示 */
    OLED_Flush(&oled);

    /* 7. 获取 OLED 状态 */
    OLED_GetStatus(&oled);

    /* 8. 关闭 OLED */
    OLED_Disable(&oled);

    return 0;
}