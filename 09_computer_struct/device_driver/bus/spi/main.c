#include <stdio.h>

#include "spi.h"
#include "spi_device.h"

int main(void)
{
    uint8_t value;

    spi_init();

    spi_write_reg(
        0x10,
        0x55);

    spi_read_reg(
        0x10,
        &value);

    printf(
        "reg=0x10 value=0x%02X\n",
        value);

    return 0;
}