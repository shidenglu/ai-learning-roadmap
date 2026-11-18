/* main.c */

#include "can.h"

int main(void)
{
    can_msg_t msg =
    {
        .id  = 0x123,
        .dlc = 4,
        .data = {0x11, 0x22, 0x33, 0x44}
    };

    can_init(500000);

    can_send(&msg);

    while (1)
    {
        can_msg_t rx;

        if (can_recv(&rx) == 0)
        {
            /* 接收数据处理 */
        }
    }

    return 0;
}