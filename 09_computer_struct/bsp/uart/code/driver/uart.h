#ifndef UART_H
#define UART_H

#include <stdint.h>

typedef enum
{
    UART_OK = 0,
    UART_ERROR
} uart_status_t;

typedef struct
{
    uint32_t baudrate;
    uint8_t data_bits;
    uint8_t stop_bits;
    uint8_t parity;
} uart_config_t;

uart_status_t uart_init(uart_config_t *cfg);

void uart_send_char(char ch);

void uart_send_string(const char *str);

int uart_receive_char(char *ch);

#endif