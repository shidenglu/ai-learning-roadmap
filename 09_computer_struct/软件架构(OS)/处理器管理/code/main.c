/**
 * 处理器管理（进程管理）完整 Demo
 * 
 * 功能：
 *   1. 进程控制块（PCB）定义
 *   2. 进程创建与销毁
 *   3. 就绪队列管理
 *   4. 多种调度算法（FCFS、SJF、RR、优先级）
 *   5. 进程状态转换
 *   6. 时间片模拟
 *
 * 编译：gcc -o process_manager process_manager.c
 * 运行：./process_manager
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/* ==================== 宏定义 ==================== */

#define MAX_PROCESSES   20      // 最大进程数
#define MAX_NAME_LEN    32      // 进程名最大长度
#define TIME_QUANTUM    3       // 时间片大小（RR调度）
#define MAX_READY_QUEUE 64      // 就绪队列最大容量

/* ==================== 枚举与结构体 ==================== */

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

// 就绪队列（循环链表）
typedef struct {
    PCB *head;
    PCB *tail;
    int count;
} ReadyQueue;

// CPU 模拟状态
typedef struct {
    PCB *current_process;           // 当前运行的进程
    int current_time;               // 当前系统时间
    int total_time;                 // 总运行时间
    PCB *process_table[MAX_PROCESSES]; // 进程表
    int process_count;              // 进程总数
    ReadyQueue ready_queue;         // 就绪队列
    SchedAlgorithm algorithm;       // 当前调度算法
} CPU;

/* ==================== 全局变量 ==================== */

static CPU cpu;
static int next_pid = 1;

/* ==================== 工具函数 ==================== */

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

void print_separator(void) {
    printf("============================================================"
           "========================\n");
}

void print_thin_separator(void) {
    printf("------------------------------------------------------------"
           "------------------------\n");
}

/* ==================== 进程创建与销毁 ==================== */

/**
 * 创建进程
 */
PCB* create_process(const char *name, int arrival_time, int burst_time, int priority) {
    if (cpu.process_count >= MAX_PROCESSES) {
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

    cpu.process_table[cpu.process_count++] = pcb;

    printf("[CREATE] PID=%d  Name=%-10s  Arrival=%d  Burst=%d  Priority=%d\n",
           pcb->pid, pcb->name, pcb->arrival_time, pcb->burst_time, pcb->priority);

    return pcb;
}

/**
 * 销毁进程（释放资源）
 */
void destroy_process(PCB *pcb) {
    if (!pcb) return;
    pcb->state = STATE_TERMINATED;
    printf("[DESTROY] PID=%d  Name=%s  完成时间=%d  周转时间=%d  等待时间=%d\n",
           pcb->pid, pcb->name, pcb->finish_time,
           pcb->turnaround_time, pcb->wait_time);
}

/* ==================== 就绪队列操作 ==================== */

/**
 * 初始化就绪队列
 */
void init_ready_queue(ReadyQueue *queue) {
    queue->head = NULL;
    queue->tail = NULL;
    queue->count = 0;
}

/**
 * 将就绪队列插入到合适位置（按优先级/到达时间排序）
 */
void enqueue_sorted(ReadyQueue *queue, PCB *pcb, SchedAlgorithm alg) {
    pcb->state = STATE_READY;
    pcb->next = NULL;

    if (queue->count == 0) {
        queue->head = pcb;
        queue->tail = pcb;
        queue->count++;
        return;
    }

    // 根据算法决定插入位置
    if (alg == SCHED_SJF) {
        // 短作业优先：按剩余时间排序
        if (pcb->remaining_time < queue->head->remaining_time) {
            pcb->next = queue->head;
            queue->head = pcb;
            queue->count++;
            return;
        }
        PCB *curr = queue->head;
        while (curr->next && curr->next->remaining_time <= pcb->remaining_time) {
            curr = curr->next;
        }
        pcb->next = curr->next;
        curr->next = pcb;
        if (curr == queue->tail) queue->tail = pcb;
        queue->count++;
    } else if (alg == SCHED_PRIORITY) {
        // 优先级调度：按优先级数值排序（小的优先）
        if (pcb->priority < queue->head->priority) {
            pcb->next = queue->head;
            queue->head = pcb;
            queue->count++;
            return;
        }
        PCB *curr = queue->head;
        while (curr->next && curr->next->priority <= pcb->priority) {
            curr = curr->next;
        }
        pcb->next = curr->next;
        curr->next = pcb;
        if (curr == queue->tail) queue->tail = pcb;
        queue->count++;
    } else {
        // FCFS / RR：尾部插入
        queue->tail->next = pcb;
        queue->tail = pcb;
        queue->count++;
    }
}

/**
 * 从就绪队列头部取出进程
 */
PCB* dequeue(ReadyQueue *queue) {
    if (queue->count == 0) return NULL;

    PCB *pcb = queue->head;
    queue->head = queue->head->next;
    if (queue->count == 1) queue->tail = NULL;
    pcb->next = NULL;
    queue->count--;
    return pcb;
}

/**
 * 将就绪队列尾部进程移到头部（RR调度用）
 */
void move_tail_to_head(ReadyQueue *queue) {
    if (queue->count <= 1) return;

    // 找到倒数第二个节点
    PCB *prev = queue->head;
    while (prev->next != queue->tail) {
        prev = prev->next;
    }

    PCB *tail_node = queue->tail;
    prev->next = NULL;
    queue->tail = prev;

    tail_node->next = queue->head;
    queue->head = tail_node;
}

/**
 * 打印就绪队列
 */
void print_ready_queue(ReadyQueue *queue) {
    if (queue->count == 0) {
        printf("  [就绪队列为空]\n");
        return;
    }
    printf("  就绪队列 (%d个进程): ", queue->count);
    PCB *curr = queue->head;
    while (curr) {
        printf("P%d(%s)", curr->pid, curr->name);
        if (curr->next) printf(" -> ");
        curr = curr->next;
    }
    printf("\n");
}

/* ==================== 调度器 ==================== */

/**
 * 将就绪队列中的进程按FCFS排序
 */
void sort_queue_fcfs(ReadyQueue *queue) {
    // 简单冒泡排序（按到达时间）
    if (queue->count <= 1) return;

    // 转为数组排序
    PCB *arr[MAX_READY_QUEUE];
    int n = 0;
    PCB *curr = queue->head;
    while (curr && n < MAX_READY_QUEUE) {
        arr[n++] = curr;
        curr = curr->next;
    }

    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (arr[j]->arrival_time > arr[j + 1]->arrival_time) {
                PCB *temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }

    // 重建链表
    queue->head = arr[0];
    for (int i = 0; i < n - 1; i++) {
        arr[i]->next = arr[i + 1];
    }
    arr[n - 1]->next = NULL;
    queue->tail = arr[n - 1];
}

/**
 * 将就绪队列中的进程按SJF排序
 */
void sort_queue_sjf(ReadyQueue *queue) {
    if (queue->count <= 1) return;

    PCB *arr[MAX_READY_QUEUE];
    int n = 0;
    PCB *curr = queue->head;
    while (curr && n < MAX_READY_QUEUE) {
        arr[n++] = curr;
        curr = curr->next;
    }

    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (arr[j]->burst_time > arr[j + 1]->burst_time) {
                PCB *temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }

    queue->head = arr[0];
    for (int i = 0; i < n - 1; i++) {
        arr[i]->next = arr[i + 1];
    }
    arr[n - 1]->next = NULL;
    queue->tail = arr[n - 1];
}

/**
 * 将就绪队列中的进程按优先级排序
 */
void sort_queue_priority(ReadyQueue *queue) {
    if (queue->count <= 1) return;

    PCB *arr[MAX_READY_QUEUE];
    int n = 0;
    PCB *curr = queue->head;
    while (curr && n < MAX_READY_QUEUE) {
        arr[n++] = curr;
        curr = curr->next;
    }

    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (arr[j]->priority > arr[j + 1]->priority) {
                PCB *temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }

    queue->head = arr[0];
    for (int i = 0; i < n - 1; i++) {
        arr[i]->next = arr[i + 1];
    }
    arr[n - 1]->next = NULL;
    queue->tail = arr[n - 1];
}

/**
 * 调度器：选择下一个运行的进程
 */
PCB* scheduler(void) {
    if (cpu.ready_queue.count == 0) return NULL;

    switch (cpu.algorithm) {
        case SCHED_FCFS:
            sort_queue_fcfs(&cpu.ready_queue);
            break;
        case SCHED_SJF:
            sort_queue_sjf(&cpu.ready_queue);
            break;
        case SCHED_PRIORITY:
            sort_queue_priority(&cpu.ready_queue);
            break;
        case SCHED_RR:
            // RR不需要排序，FIFO即可
            break;
    }

    return dequeue(&cpu.ready_queue);
}

/* ==================== CPU 模拟执行 ==================== */

/**
 * 检查是否有新进程到达
 */
void check_new_arrivals(void) {
    for (int i = 0; i < cpu.process_count; i++) {
        PCB *pcb = cpu.process_table[i];
        if (pcb->state == STATE_NEW && pcb->arrival_time <= cpu.current_time) {
            printf("  [T=%2d] 进程 P%d(%s) 到达，加入就绪队列\n",
                   cpu.current_time, pcb->pid, pcb->name);
            enqueue_sorted(&cpu.ready_queue, pcb, cpu.algorithm);
        }
    }
}

/**
 * 模拟一个时间单位的CPU执行
 */
void execute_one_tick(PCB *pcb) {
    if (!pcb) return;

    pcb->remaining_time--;

    if (pcb->start_time == -1) {
        pcb->start_time = cpu.current_time;
        pcb->response_time = cpu.current_time - pcb->arrival_time;
    }

    printf("  [T=%2d] P%d(%s) 执行中... 剩余时间=%d\n",
           cpu.current_time, pcb->pid, pcb->name, pcb->remaining_time);

    if (pcb->remaining_time <= 0) {
        // 进程执行完毕
        pcb->state = STATE_TERMINATED;
        pcb->finish_time = cpu.current_time + 1;
        pcb->turnaround_time = pcb->finish_time - pcb->arrival_time;
        pcb->wait_time = pcb->turnaround_time - pcb->burst_time;
        printf("  [T=%2d] P%d(%s) 执行完毕！周转时间=%d 等待时间=%d\n",
               cpu.current_time + 1, pcb->pid, pcb->name,
               pcb->turnaround_time, pcb->wait_time);
    }
}

/**
 * 运行调度模拟
 */
void run_simulation(void) {
    printf("\n");
    print_separator();
    printf("  开始调度模拟 | 算法: %s\n", algorithm_to_string(cpu.algorithm));
    print_separator();

    cpu.current_time = 0;
    int completed = 0;
    int total_processes = cpu.process_count;

    while (completed < total_processes) {
        // 1. 检查新到达的进程
        check_new_arrivals();

        // 2. 如果当前没有运行进程，调度一个
        if (!cpu.current_process) {
            cpu.current_process = scheduler();
            if (cpu.current_process) {
                cpu.current_process->state = STATE_RUNNING;
                printf("  [T=%2d] 调度: P%d(%s) 开始运行\n",
                       cpu.current_time, cpu.current_process->pid,
                       cpu.current_process->name);
            }
        }

        // 3. 如果有进程在运行
        if (cpu.current_process) {
            execute_one_tick(cpu.current_process);

            if (cpu.current_process->state == STATE_TERMINATED) {
                completed++;
                cpu.current_process = NULL;
            } else if (cpu.algorithm == SCHED_RR) {
                // RR调度：检查时间片是否用完
                int executed = cpu.current_process->burst_time -
                               cpu.current_process->remaining_time;
                int since_last_switch = executed % TIME_QUANTUM;

                if (since_last_switch == 0 && cpu.current_process->remaining_time > 0) {
                    // 时间片用完，放回就绪队列尾部
                    printf("  [T=%2d] P%d(%s) 时间片用完，放回就绪队列\n",
                           cpu.current_time + 1, cpu.current_process->pid,
                           cpu.current_process->name);
                    cpu.current_process->state = STATE_READY;
                    enqueue_sorted(&cpu.ready_queue, cpu.current_process, cpu.algorithm);
                    cpu.current_process = NULL;
                }
            }
        } else {
            // 没有进程可运行（空闲）
            printf("  [T=%2d] CPU 空闲\n", cpu.current_time);
        }

        // 4. 打印就绪队列状态
        if (cpu.ready_queue.count > 0) {
            print_ready_queue(&cpu.ready_queue);
        }

        cpu.current_time++;

        // 安全检查：防止死循环
        if (cpu.current_time > 1000) {
            printf("[ERROR] 模拟超时，强制退出\n");
            break;
        }
    }

    cpu.total_time = cpu.current_time;
}

/* ==================== 统计输出 ==================== */

void print_statistics(void) {
    printf("\n");
    print_separator();
    printf("  调度统计报告 | 算法: %s\n", algorithm_to_string(cpu.algorithm));
    print_separator();

    printf("\n  %-6s %-12s %-8s %-8s %-8s %-10s %-10s %-8s\n",
           "PID", "名称", "到达", "服务", "完成", "周转", "等待", "响应");
    print_thin_separator();

    float total_turnaround = 0;
    float total_wait = 0;
    float total_response = 0;

    for (int i = 0; i < cpu.process_count; i++) {
        PCB *p = cpu.process_table[i];
        printf("  %-6d %-12s %-8d %-8d %-8d %-10d %-10d %-8d\n",
               p->pid, p->name, p->arrival_time, p->burst_time,
               p->finish_time, p->turnaround_time, p->wait_time,
               p->response_time);

        total_turnaround += p->turnaround_time;
        total_wait += p->wait_time;
        total_response += p->response_time;
    }

    print_thin_separator();
    printf("  平均周转时间: %.2f\n", total_turnaround / cpu.process_count);
    printf("  平均等待时间: %.2f\n", total_wait / cpu.process_count);
    printf("  平均响应时间: %.2f\n", total_response / cpu.process_count);
    printf("  总完成时间:   %d\n", cpu.total_time);
    printf("  CPU利用率:    %.1f%%\n",
           (1.0 - (float)0 / cpu.total_time) * 100); // 简化计算
    print_separator();
}

/**
 * 打印甘特图
 */
void print_gantt_chart(void) {
    printf("\n  甘特图:\n  ");
    for (int t = 0; t <= cpu.total_time; t++) {
        printf("%-4d", t);
    }
    printf("\n  ");
    for (int t = 0; t < cpu.total_time; t++) {
        // 找到该时间片运行的进程
        char found = 0;
        for (int i = 0; i < cpu.process_count; i++) {
            PCB *p = cpu.process_table[i];
            if (p->start_time <= t && p->finish_time > t) {
                printf("|P%-3d", p->pid);
                found = 1;
                break;
            }
        }
        if (!found) printf("|   ");
    }
    printf("|\n");
}

/* ==================== 系统初始化与清理 ==================== */

void init_cpu(SchedAlgorithm alg) {
    memset(&cpu, 0, sizeof(CPU));
    init_ready_queue(&cpu.ready_queue);
    cpu.algorithm = alg;
    next_pid = 1;
}

void cleanup(void) {
    for (int i = 0; i < cpu.process_count; i++) {
        if (cpu.process_table[i]) {
            free(cpu.process_table[i]);
            cpu.process_table[i] = NULL;
        }
    }
}

/* ==================== 测试用例 ==================== */

void test_case_1(void) {
    printf("\n\n");
    print_separator();
    printf("  测试用例 1: FCFS 调度\n");
    print_separator();

    init_cpu(SCHED_FCFS);

    create_process("init",    0, 5, 3);
    create_process("system",  1, 3, 1);
    create_process("shell",   2, 8, 2);
    create_process("editor",  3, 2, 4);

    run_simulation();
    print_statistics();
    print_gantt_chart();
    cleanup();
}

void test_case_2(void) {
    printf("\n\n");
    print_separator();
    printf("  测试用例 2: SJF 调度\n");
    print_separator();

    init_cpu(SCHED_SJF);

    create_process("init",    0, 5, 3);
    create_process("system",  1, 3, 1);
    create_process("shell",   2, 8, 2);
    create_process("editor",  3, 2, 4);

    run_simulation();
    print_statistics();
    print_gantt_chart();
    cleanup();
}

void test_case_3(void) {
    printf("\n\n");
    print_separator();
    printf("  测试用例 3: RR 调度 (时间片=%d)\n", TIME_QUANTUM);
    print_separator();

    init_cpu(SCHED_RR);

    create_process("init",    0, 5, 3);
    create_process("system",  1, 3, 1);
    create_process("shell",   2, 8, 2);
    create_process("editor",  3, 2, 4);

    run_simulation();
    print_statistics();
    print_gantt_chart();
    cleanup();
}

void test_case_4(void) {
    printf("\n\n");
    print_separator();
    printf("  测试用例 4: 优先级调度\n");
    print_separator();

    init_cpu(SCHED_PRIORITY);

    create_process("init",    0, 5, 3);
    create_process("system",  1, 3, 1);
    create_process("shell",   2, 8, 2);
    create_process("editor",  3, 2, 4);

    run_simulation();
    print_statistics();
    print_gantt_chart();
    cleanup();
}

void test_case_5(void) {
    printf("\n\n");
    print_separator();
    printf("  测试用例 5: 多进程 RR 调度（模拟真实场景）\n");
    print_separator();

    init_cpu(SCHED_RR);

    create_process("nginx",   0, 10, 2);
    create_process("mysql",   0,  6, 1);
    create_process("redis",   1,  4, 1);
    create_process("python",  2,  8, 3);
    create_process("node",    3,  3, 2);
    create_process("cron",    5,  2, 4);

    run_simulation();
    print_statistics();
    print_gantt_chart();
    cleanup();
}

/* ==================== 主函数 ==================== */

int main(void) {
    printf("\n");
    print_separator();
    printf("       处理器管理（进程调度）模拟器 Demo\n");
    printf("       Process Management & CPU Scheduling\n");
    print_separator();

    test_case_1();   // FCFS
    test_case_2();   // SJF
    test_case_3();   // RR
    test_case_4();   // Priority
    test_case_5();   // 多进程 RR

    printf("\n");
    print_separator();
    printf("  所有测试完成！\n");
    print_separator();
    printf("\n");

    return 0;
}
