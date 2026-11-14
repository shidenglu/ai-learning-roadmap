#ifndef __I2C_H__
#define __I2C_H__

#include <stdint.h>

/* IIC初始化 */
void i2c_init(void);

/* 基础操作 */
void i2c_start(void);
void i2c_stop(void);

void i2c_write_byte(uint8_t data);
uint8_t i2c_read_byte(uint8_t ack);

/* 寄存器读写接口 */
int i2c_write(uint8_t dev_addr,
              uint8_t reg_addr,
              uint8_t data);

int i2c_read(uint8_t dev_addr,
             uint8_t reg_addr,
             uint8_t *data);

#endif