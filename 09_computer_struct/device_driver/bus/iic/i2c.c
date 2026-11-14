#include "i2c.h"

/* 模拟IIC寄存器 */
static volatile uint32_t I2C_CTRL;
static volatile uint32_t I2C_DATA;
static volatile uint32_t I2C_STATUS;

/* 初始化 */
void i2c_init(void)
{
    /* GPIO配置 */
    /* 时钟配置 */
    /* IIC使能 */

    I2C_CTRL = 0x01;
}

/* START信号 */
void i2c_start(void)
{
    I2C_CTRL |= (1 << 1);
}

/* STOP信号 */
void i2c_stop(void)
{
    I2C_CTRL |= (1 << 2);
}

/* 发送1字节 */
void i2c_write_byte(uint8_t data)
{
    I2C_DATA = data;

    while (!(I2C_STATUS & 0x01))
    {
    }
}

/* 接收1字节 */
uint8_t i2c_read_byte(uint8_t ack)
{
    while (!(I2C_STATUS & 0x02))
    {
    }

    if (ack)
    {
        I2C_CTRL |= (1 << 3);
    }
    else
    {
        I2C_CTRL &= ~(1 << 3);
    }

    return (uint8_t)I2C_DATA;
}

/* 写寄存器 */
int i2c_write(uint8_t dev_addr,
              uint8_t reg_addr,
              uint8_t data)
{
    i2c_start();

    i2c_write_byte(dev_addr << 1);
    i2c_write_byte(reg_addr);
    i2c_write_byte(data);

    i2c_stop();

    return 0;
}

/* 读寄存器 */
int i2c_read(uint8_t dev_addr,
             uint8_t reg_addr,
             uint8_t *data)
{
    i2c_start();

    i2c_write_byte(dev_addr << 1);
    i2c_write_byte(reg_addr);

    i2c_start();

    i2c_write_byte((dev_addr << 1) | 0x01);

    *data = i2c_read_byte(0);

    i2c_stop();

    return 0;
}