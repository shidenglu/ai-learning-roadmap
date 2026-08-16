#ifndef QUEUE_H
#define QUEUE_H

#include "pcb.h"

#define MAX_READY_QUEUE 64

/* ==================== 结构体 ==================== */

// 就绪队列（链表）
typedef struct {
    PCB *head;
    PCB *tail;
    int count;
} ReadyQueue;

/* ==================== 函数声明 ==================== */

void init_ready_queue(ReadyQueue *queue);
void enqueue_sorted(ReadyQueue *queue, PCB *pcb, SchedAlgorithm alg);
PCB* dequeue(ReadyQueue *queue);
void move_tail_to_head(ReadyQueue *queue);
void print_ready_queue(ReadyQueue *queue);
void sort_queue_fcfs(ReadyQueue *queue);
void sort_queue_sjf(ReadyQueue *queue);
void sort_queue_priority(ReadyQueue *queue);

#endif /* QUEUE_H */
