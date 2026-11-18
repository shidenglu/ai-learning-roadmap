main.c
   ↓
pcie.c

   ↓

pcie_rc.c
   ├── PHY初始化
   ├── Link Training
   └── Link Up

pcie_cfg.c
   ├── 配置空间读
   └── 配置空间写

pcie_scan.c
   ├── Bus Scan
   ├── Vendor ID
   ├── Device ID
   └── BAR发现