#include "spi_hw.h"

/* 模拟SPI寄存器 */

static volatile uint32_t SPI_CTRL;
static volatile uint32_t SPI_STATUS;
static volatile uint32_t SPI_DATA;

void spi_hw_init(void)
{
    /*
     * GPIO配置
     * SCLK
     * MOSI
     * MISO
     * CS
     */

    SPI_CTRL = 0x01;
}

uint8_t spi_hw_transfer(uint8_t data)
{
    SPI_DATA = data;

    while (!(SPI_STATUS & 0x01))
    {
    }

    return (uint8_t)SPI_DATA;
}

void spi_hw_cs_low(void)
{
    /* GPIO输出低 */
}

void spi_hw_cs_high(void)
{
    /* GPIO输出高 */
}