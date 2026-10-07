# 磁盘、接口、总线、协议关系表

| 层次 | 名称 | 作用 | 常见类型 |
|--------|--------|--------|--------|
| 存储介质 | NAND Flash | 实际存储数据 | TLC、QLC、MLC |
| 存储设备 | SSD | 固态硬盘 | SATA SSD、NVMe SSD |
| 存储设备 | HDD | 机械硬盘 | SATA HDD、SAS HDD |
| 控制协议 | AHCI | SATA设备访问协议 | SATA SSD、SATA HDD |
| 控制协议 | NVMe | SSD高速访问协议 | NVMe SSD |
| 控制协议 | SAS Protocol | 企业级磁盘协议 | SAS HDD、SAS SSD |
| 总线 | SATA | 存储总线标准 | SATA SSD、SATA HDD |
| 总线 | PCIe | 高速通用总线 | NVMe SSD |
| 总线 | SAS | 企业级存储总线 | SAS HDD、SAS SSD |
| 物理接口 | SATA接口 | SATA设备连接接口 | 2.5寸SSD、HDD |
| 物理接口 | M.2接口 | 小型高速接口 | M.2 SATA SSD、M.2 NVMe SSD |
| 物理接口 | U.2接口 | 企业级PCIe接口 | 企业级NVMe SSD |
| 物理接口 | PCIe插槽 | 扩展卡接口 | PCIe SSD |
| 主控 | SSD Controller | 管理Flash读写 | 三星、群联、慧荣等主控 |
| 主控 | HDD Controller | 管理磁头与盘片 | HDD内部控制器 |

---

# 常见组合关系

| 产品 | 接口 | 总线 | 协议 |
|--------|--------|--------|--------|
| 2.5寸 SATA SSD | SATA | SATA | AHCI |
| M.2 SATA SSD | M.2 | SATA | AHCI |
| M.2 NVMe SSD | M.2 | PCIe | NVMe |
| U.2 NVMe SSD | U.2 | PCIe | NVMe |
| PCIe SSD扩展卡 | PCIe | PCIe | NVMe |
| SATA HDD | SATA | SATA | AHCI |
| SAS HDD | SAS | SAS | SAS |
| SAS SSD | SAS | SAS | SAS |

---

# 最常见的三种磁盘

| 磁盘类型 | 接口 | 总线 | 协议 | 典型速度 |
|--------|--------|--------|--------|--------|
| SATA HDD | SATA | SATA | AHCI | 100~250 MB/s |
| SATA SSD | SATA | SATA | AHCI | 500~550 MB/s |
| NVMe SSD | M.2 | PCIe x4 | NVMe | 3000~15000 MB/s |

---

# 体系结构视角

```text
应用程序
    ↓
文件系统
    ↓
块设备驱动
    ↓
AHCI / NVMe
    ↓
SATA / PCIe
    ↓
SATA接口 / M.2接口 / U.2接口
    ↓
SSD控制器 / HDD控制器
    ↓
NAND Flash 或 磁盘
```

---

# 一句话总结

| 名称 | 本质 |
|--------|--------|
| HDD | 存储设备 |
| SSD | 存储设备 |
| SATA | 总线标准 + 接口标准 |
| PCIe | 总线 |
| AHCI | SATA设备访问协议 |
| NVMe | SSD高速访问协议 |
| M.2 | 物理接口 |
| U.2 | 物理接口 |
| NAND Flash | 存储介质 |

典型组合：

SATA SSD = SSD + SATA接口 + SATA总线 + AHCI协议

NVMe SSD = SSD + M.2接口 + PCIe总线 + NVMe协议