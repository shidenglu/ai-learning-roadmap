# SPI驱动调用流程

```text
main()
  ↓
spi_init()
  ↓
SPI控制器初始化
  ↓
拉低CS
  ↓
发送寄存器地址
  ↓
发送/接收数据
  ↓
拉高CS
```

# SPI总线结构

```text
          SPI Master
               │
      ┌────────┼────────┐
      │        │        │
     SCLK     MOSI     MISO
      │        │        │
      └────────┼────────┘
               │
            SPI Slave
               │
              CS
```

# BSP中的进一步拆分

大型项目一般继续拆分：

```text
spi/
├── spi.c
├── spi.h
├── spi_hw.c
├── spi_irq.c
├── spi_dma.c
├── spi_device.c
├── spi_flash.c
├── spi_eeprom.c
└── spi_sensor.c
```

对应：

```text
SPI Core
   ↓
SPI Controller Driver
   ↓
SPI Device Driver
   ├── Flash
   ├── EEPROM
   ├── ADC
   ├── Sensor
   └── LCD
```