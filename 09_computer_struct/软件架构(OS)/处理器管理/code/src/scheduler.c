#include "../include/scheduler.h"

PCB* scheduler(ReadyQueue *queue, SchedAlgorithm alg) {
    if (queue->count == 0) return NULL;

    switch (alg) {
        case SCHED_FCFS:
            sort_queue_fcfs(queue);
            break;
        case SCHED_SJF:
            sort_queue_sjf(queue);
            break;
        case SCHED_PRIORITY:
            sort_queue_priority(queue);
            break;
        case SCHED_RR:
            // RR 不需要排序，FIFO 即可
            break;
    }

    return dequeue(queue);
}
