#include "../include/cpu.h"
#include "../include/scheduler.h"

/* 全局进程表（供 pcb.c 使用） */
PCB *g_process_table[MAX_PROCESSES];
int g_process_count = 0;

void init_cpu(CPU *cpu, SchedAlgorithm alg) {
    memset(cpu, 0, sizeof(CPU));
    init_ready_queue(&cpu->ready_queue);
    cpu->algorithm = alg;
    g_process_count = 0;
    memset(g_process_table, 0, sizeof(g_process_table));
}

void check_new_arrivals(CPU *cpu) {
    for (int i = 0; i < cpu->process_count; i++) {
        PCB *pcb = cpu->process_table[i];
        if (pcb->state == STATE_NEW && pcb->arrival_time <= cpu->current_time) {
            printf("  [T=%2d] 进程 P%d(%s) 到达，加入就绪队列\n",
                   cpu->current_time, pcb->pid, pcb->name);
            enqueue_sorted(&cpu->ready_queue, pcb, cpu->algorithm);
        }
    }
}

void execute_one_tick(CPU *cpu, PCB *pcb) {
    if (!pcb) return;

    pcb->remaining_time--;

    if (pcb->start_time == -1) {
        pcb->start_time = cpu->current_time;
        pcb->response_time = cpu->current_time - pcb->arrival_time;
    }

    printf("  [T=%2d] P%d(%s) 执行中... 剩余时间=%d\n",
           cpu->current_time, pcb->pid, pcb->name, pcb->remaining_time);

    if (pcb->remaining_time <= 0) {
        pcb->state = STATE_TERMINATED;
        pcb->finish_time = cpu->current_time + 1;
        pcb->turnaround_time = pcb->finish_time - pcb->arrival_time;
        pcb->wait_time = pcb->turnaround_time - pcb->burst_time;
        printf("  [T=%2d] P%d(%s) 执行完毕！周转时间=%d 等待时间=%d\n",
               cpu->current_time + 1, pcb->pid, pcb->name,
               pcb->turnaround_time, pcb->wait_time);
    }
}

void run_simulation(CPU *cpu) {
    printf("\n");
    printf("============================================================"
           "========================\n");
    printf("  开始调度模拟 | 算法: %s\n", algorithm_to_string(cpu->algorithm));
    printf("============================================================"
           "========================\n");

    cpu->current_time = 0;
    int completed = 0;
    int total_processes = cpu->process_count;

    while (completed < total_processes) {
        // 1. 检查新到达的进程
        check_new_arrivals(cpu);

        // 2. 如果当前没有运行进程，调度一个
        if (!cpu->current_process) {
            cpu->current_process = scheduler(&cpu->ready_queue, cpu->algorithm);
            if (cpu->current_process) {
                cpu->current_process->state = STATE_RUNNING;
                printf("  [T=%2d] 调度: P%d(%s) 开始运行\n",
                       cpu->current_time, cpu->current_process->pid,
                       cpu->current_process->name);
            }
        }

        // 3. 如果有进程在运行
        if (cpu->current_process) {
            execute_one_tick(cpu, cpu->current_process);

            if (cpu->current_process->state == STATE_TERMINATED) {
                completed++;
                cpu->current_process = NULL;
            } else if (cpu->algorithm == SCHED_RR) {
                // RR调度：检查时间片是否用完
                int executed = cpu->current_process->burst_time -
                               cpu->current_process->remaining_time;
                if (executed % TIME_QUANTUM == 0 && cpu->current_process->remaining_time > 0) {
                    printf("  [T=%2d] P%d(%s) 时间片用完，放回就绪队列\n",
                           cpu->current_time + 1, cpu->current_process->pid,
                           cpu->current_process->name);
                    cpu->current_process->state = STATE_READY;
                    enqueue_sorted(&cpu->ready_queue, cpu->current_process, cpu->algorithm);
                    cpu->current_process = NULL;
                }
            }
        } else {
            printf("  [T=%2d] CPU 空闲\n", cpu->current_time);
        }

        // 4. 打印就绪队列状态
        if (cpu->ready_queue.count > 0) {
            print_ready_queue(&cpu->ready_queue);
        }

        cpu->current_time++;

        // 安全检查：防止死循环
        if (cpu->current_time > 1000) {
            printf("[ERROR] 模拟超时，强制退出\n");
            break;
        }
    }

    cpu->total_time = cpu->current_time;
}

void cleanup_cpu(CPU *cpu) {
    for (int i = 0; i < cpu->process_count; i++) {
        if (cpu->process_table[i]) {
            free(cpu->process_table[i]);
            cpu->process_table[i] = NULL;
        }
    }
    cpu->process_count = 0;
}
