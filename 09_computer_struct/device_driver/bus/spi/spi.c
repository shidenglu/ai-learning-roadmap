#include "spi.h"
#include "spi_hw.h"

void spi_init(void)
{
    spi_hw_init();
}

uint8_t spi_transfer(uint8_t data)
{
    return spi_hw_transfer(data);
}

void spi_cs_low(void)
{
    spi_hw_cs_low();
}

void spi_cs_high(void)
{
    spi_hw_cs_high();
}