// 模拟寄存器访问
#include "uart_hw.h"

#define UART_BASE      0x40000000

#define UART_DR        (*(volatile uint32_t *)(UART_BASE + 0x00))
#define UART_SR        (*(volatile uint32_t *)(UART_BASE + 0x04))
#define UART_BAUD      (*(volatile uint32_t *)(UART_BASE + 0x08))

#define UART_TX_EMPTY  (1 << 0)
#define UART_RX_READY  (1 << 1)

void uart_hw_init(uint32_t baudrate)
{
    UART_BAUD = baudrate;
}

int uart_hw_tx_ready(void)
{
    return (UART_SR & UART_TX_EMPTY);
}

int uart_hw_rx_ready(void)
{
    return (UART_SR & UART_RX_READY);
}

void uart_hw_send(uint8_t data)
{
    UART_DR = data;
}

uint8_t uart_hw_receive(void)
{
    return (uint8_t)UART_DR;
}