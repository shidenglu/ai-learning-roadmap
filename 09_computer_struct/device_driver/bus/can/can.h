/* can.h */

#ifndef __CAN_H__
#define __CAN_H__

#include <stdint.h>

#define CAN_MAX_DATA_LEN 8

typedef struct
{
    uint32_t id;
    uint8_t  dlc;
    uint8_t  data[CAN_MAX_DATA_LEN];
} can_msg_t;

int  can_init(uint32_t baudrate);
int  can_send(const can_msg_t *msg);
int  can_recv(can_msg_t *msg);
void can_irq_handler(void);

#endif