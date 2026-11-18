#ifndef PCB_H
#define PCB_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* ==================== 宏定义 ==================== */

#define MAX_PROCESSES   20
#define MAX_NAME_LEN    32

/* ==================== 枚举 ==================== */

// 进程状态
typedef enum {
    STATE_NEW,          // 新建
    STATE_READY,        // 就绪
    STATE_RUNNING,      // 运行
    STATE_WAITING,      // 等待（阻塞）
    STATE_TERMINATED    // 终止
} ProcessState;

// 调度算法
typedef enum {
    SCHED_FCFS,         // 先来先服务
    SCHED_SJF,          // 短作业优先
    SCHED_RR,           // 时间片轮转
    SCHED_PRIORITY      // 优先级调度
} SchedAlgorithm;

/* ==================== 结构体 ==================== */

// 进程控制块（PCB）
typedef struct PCB {
    int pid;                        // 进程ID
    char name[MAX_NAME_LEN];        // 进程名
    ProcessState state;             // 进程状态
    int arrival_time;               // 到达时间
    int burst_time;                 // 总CPU时间（服务时间）
    int remaining_time;             // 剩余CPU时间
    int priority;                   // 优先级（数值越小优先级越高）
    int start_time;                 // 首次执行时间
    int finish_time;                // 完成时间
    int wait_time;                  // 等待时间
    int turnaround_time;            // 周转时间
    int response_time;              // 响应时间（-1表示未响应）
    struct PCB *next;               // 链表指针
} PCB;

/* ==================== 函数声明 ==================== */

const char* state_to_string(ProcessState state);
const char* algorithm_to_string(SchedAlgorithm alg);
PCB* create_process(const char *name, int arrival_time, int burst_time, int priority);
void destroy_process(PCB *pcb);

#endif /* PCB_H */
