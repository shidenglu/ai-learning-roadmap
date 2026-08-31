#ifndef CPU_H
#define CPU_H

#include "pcb.h"
#include "queue.h"

#define TIME_QUANTUM 3  // 时间片大小（RR调度）

/* ==================== 结构体 ==================== */

// CPU 模拟状态
typedef struct {
    PCB *current_process;                       // 当前运行的进程
    int current_time;                           // 当前系统时间
    int total_time;                             // 总运行时间
    PCB *process_table[MAX_PROCESSES];          // 进程表
    int process_count;                          // 进程总数
    ReadyQueue ready_queue;                     // 就绪队列
    SchedAlgorithm algorithm;                   // 当前调度算法
} CPU;

/* ==================== 函数声明 ==================== */

void init_cpu(CPU *cpu, SchedAlgorithm alg);
void check_new_arrivals(CPU *cpu);
void execute_one_tick(CPU *cpu, PCB *pcb);
void run_simulation(CPU *cpu);
void cleanup_cpu(CPU *cpu);

#endif /* CPU_H */
