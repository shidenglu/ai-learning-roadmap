#include "../include/pcb.h"

/* 全局PID计数器 */
static int next_pid = 1;

/* 全局进程表指针（由cpu模块管理，此处仅做创建） */
extern PCB *g_process_table[MAX_PROCESSES];
extern int g_process_count;

const char* state_to_string(ProcessState state) {
    switch (state) {
        case STATE_NEW:        return "NEW";
        case STATE_READY:      return "READY";
        case STATE_RUNNING:    return "RUNNING";
        case STATE_WAITING:    return "WAITING";
        case STATE_TERMINATED: return "TERMINATED";
        default:               return "UNKNOWN";
    }
}

const char* algorithm_to_string(SchedAlgorithm alg) {
    switch (alg) {
        case SCHED_FCFS:     return "FCFS (先来先服务)";
        case SCHED_SJF:      return "SJF  (短作业优先)";
        case SCHED_RR:       return "RR   (时间片轮转)";
        case SCHED_PRIORITY: return "PRIO (优先级调度)";
        default:             return "UNKNOWN";
    }
}

PCB* create_process(const char *name, int arrival_time, int burst_time, int priority) {
    if (g_process_count >= MAX_PROCESSES) {
        printf("[ERROR] 进程表已满，无法创建新进程\n");
        return NULL;
    }

    PCB *pcb = (PCB *)malloc(sizeof(PCB));
    if (!pcb) {
        printf("[ERROR] 内存分配失败\n");
        return NULL;
    }

    pcb->pid = next_pid++;
    strncpy(pcb->name, name, MAX_NAME_LEN - 1);
    pcb->name[MAX_NAME_LEN - 1] = '\0';
    pcb->state = STATE_NEW;
    pcb->arrival_time = arrival_time;
    pcb->burst_time = burst_time;
    pcb->remaining_time = burst_time;
    pcb->priority = priority;
    pcb->start_time = -1;
    pcb->finish_time = -1;
    pcb->wait_time = 0;
    pcb->turnaround_time = 0;
    pcb->response_time = -1;
    pcb->next = NULL;

    g_process_table[g_process_count++] = pcb;

    printf("[CREATE] PID=%d  Name=%-10s  Arrival=%d  Burst=%d  Priority=%d\n",
           pcb->pid, pcb->name, pcb->arrival_time, pcb->burst_time, pcb->priority);

    return pcb;
}

void destroy_process(PCB *pcb) {
    if (!pcb) return;
    pcb->state = STATE_TERMINATED;
    printf("[DESTROY] PID=%d  Name=%s  完成时间=%d  周转时间=%d  等待时间=%d\n",
           pcb->pid, pcb->name, pcb->finish_time,
           pcb->turnaround_time, pcb->wait_time);
}
