// 负责访问硬件寄存器
#ifndef UART_HW_H
#define UART_HW_H

#include <stdint.h>

void uart_hw_init(uint32_t baudrate);

void uart_hw_send(uint8_t data);

uint8_t uart_hw_receive(void);

int uart_hw_tx_ready(void);

int uart_hw_rx_ready(void);

#endif