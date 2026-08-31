// 应用层使用
#include "../driver/uart.h"

int main(void)
{
    uart_config_t cfg =
    {
        .baudrate = 115200,
        .data_bits = 8,
        .stop_bits = 1,
        .parity = 0
    };

    uart_init(&cfg);

    uart_send_string("Hello UART!\r\n");

    while(1)
    {
        char ch;

        if(uart_receive_char(&ch) == 0)
        {
            uart_send_char(ch);
        }
    }
}