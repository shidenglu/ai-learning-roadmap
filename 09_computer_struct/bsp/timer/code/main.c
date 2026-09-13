#include <stdio.h>
#include <unistd.h>

#include "timer.h"

int main(void)
{
    printf("========== System Boot ==========\n");

    /* BSP 初始化 Timer */
    bsp_timer_init(1);     // 1 ms

    printf("\n========== System Running ==========\n");

    /* 模拟系统运行 */
    while (timer_get_tick() < 10)
    {
        /* 模拟硬件 Timer 每 1 ms 运行一次 */
        usleep(1000);

        timer_run();
    }

    printf("\n========== System Stop ==========\n");

    return 0;
}