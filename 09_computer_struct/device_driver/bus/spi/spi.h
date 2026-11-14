#ifndef __SPI_H__
#define __SPI_H__

#include <stdint.h>

void spi_init(void);

uint8_t spi_transfer(uint8_t data);

void spi_cs_low(void);
void spi_cs_high(void);

#endif