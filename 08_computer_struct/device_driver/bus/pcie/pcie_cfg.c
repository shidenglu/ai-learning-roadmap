#include "pcie_cfg.h"

#define PCIE_CFG_BASE 0x40000000UL

static inline uint32_t cfg_addr(
    uint8_t bus,
    uint8_t dev,
    uint8_t func,
    uint16_t offset)
{
    return PCIE_CFG_BASE +
           (bus  << 20) +
           (dev  << 15) +
           (func << 12) +
           offset;
}

uint32_t pcie_cfg_read32(
    uint8_t bus,
    uint8_t dev,
    uint8_t func,
    uint16_t offset)
{
    volatile uint32_t *addr =
        (volatile uint32_t *)
        cfg_addr(bus, dev, func, offset);

    return *addr;
}

void pcie_cfg_write32(
    uint8_t bus,
    uint8_t dev,
    uint8_t func,
    uint16_t offset,
    uint32_t value)
{
    volatile uint32_t *addr =
        (volatile uint32_t *)
        cfg_addr(bus, dev, func, offset);

    *addr = value;
}