#include "pcie.h"
#include "pcie_rc.h"
#include "pcie_scan.h"

void pcie_init(void)
{
    pcie_rc_init();
    pcie_scan_bus();
}