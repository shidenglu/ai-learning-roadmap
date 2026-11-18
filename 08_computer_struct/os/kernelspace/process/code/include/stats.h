#ifndef STATS_H
#define STATS_H

#include "cpu.h"

/* ==================== 函数声明 ==================== */

void print_separator(void);
void print_thin_separator(void);
void print_statistics(CPU *cpu);
void print_gantt_chart(CPU *cpu);

#endif /* STATS_H */
