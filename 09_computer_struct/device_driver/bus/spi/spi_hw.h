#ifndef __SPI_HW_H__
#define __SPI_HW_H__

#include <stdint.h>

void spi_hw_init(void);

uint8_t spi_hw_transfer(uint8_t data);

void spi_hw_cs_low(void);
void spi_hw_cs_high(void);

#endif