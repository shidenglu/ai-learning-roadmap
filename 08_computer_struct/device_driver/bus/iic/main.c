#include <stdio.h>
#include "i2c.h"

int main(void)
{
    uint8_t value;

    i2c_init();

    /* 向设备0x50寄存器0x10写入0x55 */
    i2c_write(0x50, 0x10, 0x55);

    /* 从设备0x50寄存器0x10读取 */
    i2c_read(0x50, 0x10, &value);

    printf("value = 0x%02X\n", value);

    return 0;
}