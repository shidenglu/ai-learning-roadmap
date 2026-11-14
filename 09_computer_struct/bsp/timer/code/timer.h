#ifndef TIMER_H
#define TIMER_H

#include <stdint.h>

/* BSP Timer 初始化 */
void bsp_timer_init(uint32_t period_ms);

/* 模拟硬件 Timer 运行 */
void timer_run(void);

/* Timer ISR */
void timer_isr(void);

/* 获取系统 Tick */
uint32_t timer_get_tick(void);

#endif