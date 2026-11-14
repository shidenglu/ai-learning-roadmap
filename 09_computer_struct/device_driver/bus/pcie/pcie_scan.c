#include <stdio.h>
#include "pcie_scan.h"
#include "pcie_cfg.h"

void pcie_scan_bus(void)
{
    for(int dev = 0; dev < 32; dev++)
    {
        uint32_t id;

        id = pcie_cfg_read32(
                 0,
                 dev,
                 0,
                 0x00);

        if((id & 0xFFFF) == 0xFFFF)
            continue;

        printf(
            "PCIe Device "
            "Dev=%d "
            "VID=%04X "
            "DID=%04X\n",
            dev,
            id & 0xFFFF,
            id >> 16);
    }
}