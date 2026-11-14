#ifndef __PCIE_CFG_H__
#define __PCIE_CFG_H__

#include <stdint.h>

uint32_t pcie_cfg_read32(
    uint8_t bus,
    uint8_t dev,
    uint8_t func,
    uint16_t offset);

void pcie_cfg_write32(
    uint8_t bus,
    uint8_t dev,
    uint8_t func,
    uint16_t offset,
    uint32_t value);

#endif