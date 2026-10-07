#ifndef __UART_H__
#define __UART_H__

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* 校验方式 */
typedef enum
{
    UART_PARITY_NONE = 0,
    UART_PARITY_ODD,
    UART_PARITY_EVEN
} uart_parity_t;

/* 停止位 */
typedef enum
{
    UART_STOP_1 = 1,
    UART_STOP_2 = 2
} uart_stop_bit_t;

/* 数据位 */
typedef enum
{
    UART_DATA_7BIT = 7,
    UART_DATA_8BIT = 8
} uart_data_bit_t;

/* UART配置 */
typedef struct
{
    uint32_t baudrate;
    uart_data_bit_t data_bits;
    uart_stop_bit_t stop_bits;
    uart_parity_t parity;
} uart_config_t;

/* 初始化 */
int uart_init(const uart_config_t *cfg);

/* 发送一个字符 */
void uart_putc(char ch);

/* 接收一个字符 */
char uart_getc(void);

/* 发送数据 */
int uart_write(const uint8_t *buf, uint32_t len);

/* 接收数据 */
int uart_read(uint8_t *buf, uint32_t len);

/* 字符串发送 */
void uart_puts(const char *str);

/* 中断服务函数 */
void uart_irq_handler(void);

#ifdef __cplusplus
}
#endif

#endif