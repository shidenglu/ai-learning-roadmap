#include "uart.h"

/**************************************************************************
 * UART寄存器定义
 **************************************************************************/

#define UART_BASE_ADDR     0x40000000U

#define UART_DR            (*(volatile uint32_t *)(UART_BASE_ADDR + 0x00))
#define UART_SR            (*(volatile uint32_t *)(UART_BASE_ADDR + 0x04))
#define UART_BAUD          (*(volatile uint32_t *)(UART_BASE_ADDR + 0x08))
#define UART_CR            (*(volatile uint32_t *)(UART_BASE_ADDR + 0x0C))

/**************************************************************************
 * 状态位
 **************************************************************************/

#define UART_SR_TX_EMPTY   (1U << 0)
#define UART_SR_RX_READY   (1U << 1)

/**************************************************************************
 * 控制位
 **************************************************************************/

#define UART_CR_TX_EN      (1U << 0)
#define UART_CR_RX_EN      (1U << 1)
#define UART_CR_RX_INT_EN  (1U << 2)

/**************************************************************************
 * 环形缓冲区
 **************************************************************************/

#define UART_RX_BUF_SIZE   256

static uint8_t rx_buf[UART_RX_BUF_SIZE];

static volatile uint32_t rx_head = 0;
static volatile uint32_t rx_tail = 0;

/**************************************************************************
 * 初始化
 **************************************************************************/

int uart_init(const uart_config_t *cfg)
{
    if (cfg == NULL)
    {
        return -1;
    }

    /* 配置波特率 */
    UART_BAUD = cfg->baudrate;

    /* 使能发送和接收 */
    UART_CR =
          UART_CR_TX_EN
        | UART_CR_RX_EN
        | UART_CR_RX_INT_EN;

    rx_head = 0;
    rx_tail = 0;

    return 0;
}

/**************************************************************************
 * 发送一个字符
 **************************************************************************/

void uart_putc(char ch)
{
    while (!(UART_SR & UART_SR_TX_EMPTY))
    {
    }

    UART_DR = (uint32_t)ch;
}

/**************************************************************************
 * 接收一个字符（轮询）
 **************************************************************************/

char uart_getc(void)
{
    while (!(UART_SR & UART_SR_RX_READY))
    {
    }

    return (char)UART_DR;
}

/**************************************************************************
 * 发送缓冲区
 **************************************************************************/

int uart_write(const uint8_t *buf, uint32_t len)
{
    uint32_t i;

    if (buf == NULL)
    {
        return -1;
    }

    for (i = 0; i < len; i++)
    {
        uart_putc((char)buf[i]);
    }

    return (int)len;
}

/**************************************************************************
 * 接收缓冲区
 **************************************************************************/

int uart_read(uint8_t *buf, uint32_t len)
{
    uint32_t count = 0;

    if (buf == NULL)
    {
        return -1;
    }

    while (count < len)
    {
        if (rx_head == rx_tail)
        {
            break;
        }

        buf[count++] = rx_buf[rx_tail];

        rx_tail = (rx_tail + 1) % UART_RX_BUF_SIZE;
    }

    return (int)count;
}

/**************************************************************************
 * 字符串发送
 **************************************************************************/

void uart_puts(const char *str)
{
    if (str == NULL)
    {
        return;
    }

    while (*str)
    {
        uart_putc(*str++);
    }
}

/**************************************************************************
 * UART中断处理
 **************************************************************************/

void uart_irq_handler(void)
{
    uint32_t next;
    uint8_t data;

    if (UART_SR & UART_SR_RX_READY)
    {
        data = (uint8_t)UART_DR;

        next = (rx_head + 1) % UART_RX_BUF_SIZE;

        if (next != rx_tail)
        {
            rx_buf[rx_head] = data;
            rx_head = next;
        }
    }
}