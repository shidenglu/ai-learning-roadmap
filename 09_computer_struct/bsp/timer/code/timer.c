#include <stdio.h>
#include <stdint.h>
#include "timer.h"

/* 模拟 Timer 硬件寄存器 */
typedef struct
{
    uint32_t CTRL;
    uint32_t LOAD;
    uint32_t VALUE;
    uint32_t IRQ;
} TimerRegs;

static TimerRegs timer0;

static uint32_t system_tick = 0;

/* =========================================================
 * BSP Timer 初始化
 * ========================================================= */
void bsp_timer_init(uint32_t period_ms)
{
    printf("[BSP] Timer Init\n");

    /* 1. Enable Timer Clock */
    printf("[BSP] Enable Timer Clock\n");

    /* 2. Reset Timer */
    timer0.CTRL  = 0;
    timer0.LOAD  = 0;
    timer0.VALUE = 0;
    timer0.IRQ   = 0;

    printf("[BSP] Timer Reset\n");

    /* 3. 配置 Timer 周期
     * 假设 Timer Clock = 1 MHz
     * 1 ms = 1000 个计数
     */
    timer0.LOAD = period_ms * 1000;
    timer0.VALUE = timer0.LOAD;

    printf("[BSP] Timer Period = %u ms\n", period_ms);

    /* 4. 配置 Timer IRQ */
    printf("[BSP] Register Timer ISR\n");
    printf("[BSP] Enable Timer IRQ\n");

    /* 5. Enable Timer */
    timer0.CTRL = 1;

    printf("[BSP] Timer Enable\n");
}

/* =========================================================
 * 模拟 Timer 硬件运行
 * ========================================================= */
void timer_run(void)
{
    if (!timer0.CTRL)
        return;

    if (timer0.VALUE > 0)
        timer0.VALUE--;

    /* Counter 到 0 → 产生 IRQ */
    if (timer0.VALUE == 0)
    {
        timer0.IRQ = 1;

        /* 模拟 CPU 响应 IRQ */
        timer_isr();

        /* Periodic Timer 重新装载 */
        timer0.VALUE = timer0.LOAD;
    }
}

/* =========================================================
 * Timer ISR
 * ========================================================= */
void timer_isr(void)
{
    /* 清除 Timer IRQ */
    timer0.IRQ = 0;

    /* 模拟系统 Tick */
    system_tick++;

    printf("[ISR] Timer IRQ -> tick = %u\n",
           system_tick);
}

/* =========================================================
 * 获取 Tick
 * ========================================================= */
uint32_t timer_get_tick(void)
{
    return system_tick;
}