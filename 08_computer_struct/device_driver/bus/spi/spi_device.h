#ifndef __SPI_DEVICE_H__
#define __SPI_DEVICE_H__

#include <stdint.h>

int spi_write_reg(
    uint8_t reg,
    uint8_t value);

int spi_read_reg(
    uint8_t reg,
    uint8_t *value);

#endif