# 简单结构
Application
    │
    ▼
uart.c        （驱动层）
    │
    ▼
uart_hw.c     （硬件抽象层HAL）
    │
    ▼
UART寄存器

# 实际使用

## 轮询模式

应用
  │
uart_send()
  │
while(TX_BUSY)
  │
寄存器

## 中断模式

发送：
应用
  │
写入TX RingBuffer
  │
开启TX中断
  │
ISR不断发送

接受：
UART RX中断
     │
     ▼
RX RingBuffer
     │
     ▼
应用读取

结构：
typedef struct
{
    uint8_t buffer[1024];
    uint32_t head;
    uint32_t tail;
} ring_buffer_t;

## DMA 模式

Application
      │
      ▼
uart_write()
      │
      ▼
DMA Controller
      │
      ▼
UART FIFO

# Linux风格UART驱动框架

## Linux串口驱动组成

uart_driver
    │
    ├── probe()
    ├── startup()
    ├── shutdown()
    ├── start_tx()
    ├── stop_tx()
    ├── start_rx()
    └── irq_handler()

## 核心数据结构

struct uart_port
{
    unsigned long membase;

    int irq;

    spinlock_t lock;

    struct circ_buf tx_buf;

    struct circ_buf rx_buf;
};

## 收发流程

用户程序
    │
write()
    │
tty层
    │
uart_driver
    │
uart_port
    │
UART硬件

# 真实的UART驱动框架

uart/
│
├── uart.h
├── uart.c
│
├── uart_hw.h
├── uart_hw.c
│
├── uart_irq.c
│
├── uart_dma.c
│
├── ringbuffer.c
├── ringbuffer.h
│
└── uart_test.c