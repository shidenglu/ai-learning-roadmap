/* can.c */

#include "can.h"
#include <stdio.h>

/* 模拟CAN寄存器 */
static volatile uint32_t CAN_CTRL;
static volatile uint32_t CAN_BAUD;
static volatile uint32_t CAN_STATUS;

int can_init(uint32_t baudrate)
{
    CAN_CTRL = 0;

    /* 设置波特率 */
    CAN_BAUD = baudrate;

    /* 使能CAN控制器 */
    CAN_CTRL |= 0x01;

    printf("CAN init, baudrate=%u\n", baudrate);

    return 0;
}

int can_send(const can_msg_t *msg)
{
    if (msg == 0 || msg->dlc > CAN_MAX_DATA_LEN)
        return -1;

    /* 等待发送邮箱空闲 */
    while (CAN_STATUS & 0x01)
        ;

    printf("TX ID=0x%X DLC=%u DATA=",
           msg->id,
           msg->dlc);

    for (uint8_t i = 0; i < msg->dlc; i++)
        printf("%02X ", msg->data[i]);

    printf("\n");

    /* 实际驱动中：
       1. 写ID寄存器
       2. 写DLC
       3. 写DATA
       4. 触发发送
    */

    return 0;
}

int can_recv(can_msg_t *msg)
{
    if (msg == 0)
        return -1;

    /* 没有数据 */
    if (!(CAN_STATUS & 0x02))
        return -1;

    /*
     * 实际驱动中从RX FIFO读取：
     * msg->id
     * msg->dlc
     * msg->data[]
     */

    return 0;
}

void can_irq_handler(void)
{
    /* RX中断 */
    if (CAN_STATUS & 0x02)
    {
        can_msg_t msg;

        if (can_recv(&msg) == 0)
        {
            /* 处理接收数据 */
        }
    }

    /* TX完成中断 */
    if (CAN_STATUS & 0x04)
    {
        /* 清除发送完成中断 */
    }

    /* 错误中断 */
    if (CAN_STATUS & 0x08)
    {
        /* Bus Off / ACK / CRC等错误处理 */
    }
}