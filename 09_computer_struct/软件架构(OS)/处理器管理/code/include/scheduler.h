#ifndef SCHEDULER_H
#define SCHEDULER_H

#include "pcb.h"
#include "queue.h"

/* ==================== 函数声明 ==================== */

/**
 * 调度器：根据当前算法从就绪队列中选择下一个运行的进程
 */
PCB* scheduler(ReadyQueue *queue, SchedAlgorithm alg);

#endif /* SCHEDULER_H */
