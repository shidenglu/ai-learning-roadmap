// 驱动逻辑
#include "uart.h"
#include "../hw/uart_hw.h"

uart_status_t uart_init(uart_config_t *cfg)
{
    if(cfg == 0)
    {
        return UART_ERROR;
    }

    uart_hw_init(cfg->baudrate);

    return UART_OK;
}

void uart_send_char(char ch)
{
    while(!uart_hw_tx_ready());

    uart_hw_send((uint8_t)ch);
}

void uart_send_string(const char *str)
{
    while(*str)
    {
        uart_send_char(*str++);
    }
}

int uart_receive_char(char *ch)
{
    if(!uart_hw_rx_ready())
    {
        return -1;
    }

    *ch = uart_hw_receive();

    return 0;
}