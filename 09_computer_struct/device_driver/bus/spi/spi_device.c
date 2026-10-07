#include "spi_device.h"
#include "spi.h"

int spi_write_reg(
    uint8_t reg,
    uint8_t value)
{
    spi_cs_low();

    spi_transfer(reg);
    spi_transfer(value);

    spi_cs_high();

    return 0;
}

int spi_read_reg(
    uint8_t reg,
    uint8_t *value)
{
    spi_cs_low();

    spi_transfer(reg | 0x80);

    *value = spi_transfer(0xFF);

    spi_cs_high();

    return 0;
}