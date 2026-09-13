#include <stdio.h>
#include "../include/pcb.h"
#include "../include/queue.h"
#include "../include/scheduler.h"
#include "../include/cpu.h"
#include "../include/stats.h"

/* 引用全局进程表 */
extern PCB *g_process_table[MAX_PROCESSES];
extern int g_process_count;

/* ==================== 辅助：注册进程到CPU ==================== */

static void add_process_to_cpu(CPU *cpu, const char *name,
                               int arrival, int burst, int priority) {
    PCB *pcb = create_process(name, arrival, burst, priority);
    if (pcb) {
        cpu->process_table[cpu->process_count++] = pcb;
    }
}

/* ==================== 测试用例 ==================== */

void test_fcfs(void) {
    printf("\n\n");
    print_separator();
    printf("  测试用例 1: FCFS 调度\n");
    print_separator();

    CPU cpu;
    init_cpu(&cpu, SCHED_FCFS);

    add_process_to_cpu(&cpu, "init",   0, 5, 3);
    add_process_to_cpu(&cpu, "system", 1, 3, 1);
    add_process_to_cpu(&cpu, "shell",  2, 8, 2);
    add_process_to_cpu(&cpu, "editor", 3, 2, 4);

    run_simulation(&cpu);
    print_statistics(&cpu);
    print_gantt_chart(&cpu);
    cleanup_cpu(&cpu);
}

void test_sjf(void) {
    printf("\n\n");
    print_separator();
    printf("  测试用例 2: SJF 调度\n");
    print_separator();

    CPU cpu;
    init_cpu(&cpu, SCHED_SJF);

    add_process_to_cpu(&cpu, "init",   0, 5, 3);
    add_process_to_cpu(&cpu, "system", 1, 3, 1);
    add_process_to_cpu(&cpu, "shell",  2, 8, 2);
    add_process_to_cpu(&cpu, "editor", 3, 2, 4);

    run_simulation(&cpu);
    print_statistics(&cpu);
    print_gantt_chart(&cpu);
    cleanup_cpu(&cpu);
}

void test_rr(void) {
    printf("\n\n");
    print_separator();
    printf("  测试用例 3: RR 调度 (时间片=%d)\n", TIME_QUANTUM);
    print_separator();

    CPU cpu;
    init_cpu(&cpu, SCHED_RR);

    add_process_to_cpu(&cpu, "init",   0, 5, 3);
    add_process_to_cpu(&cpu, "system", 1, 3, 1);
    add_process_to_cpu(&cpu, "shell",  2, 8, 2);
    add_process_to_cpu(&cpu, "editor", 3, 2, 4);

    run_simulation(&cpu);
    print_statistics(&cpu);
    print_gantt_chart(&cpu);
    cleanup_cpu(&cpu);
}

void test_priority(void) {
    printf("\n\n");
    print_separator();
    printf("  测试用例 4: 优先级调度\n");
    print_separator();

    CPU cpu;
    init_cpu(&cpu, SCHED_PRIORITY);

    add_process_to_cpu(&cpu, "init",   0, 5, 3);
    add_process_to_cpu(&cpu, "system", 1, 3, 1);
    add_process_to_cpu(&cpu, "shell",  2, 8, 2);
    add_process_to_cpu(&cpu, "editor", 3, 2, 4);

    run_simulation(&cpu);
    print_statistics(&cpu);
    print_gantt_chart(&cpu);
    cleanup_cpu(&cpu);
}

void test_multi_rr(void) {
    printf("\n\n");
    print_separator();
    printf("  测试用例 5: 多进程 RR 调度（模拟真实场景）\n");
    print_separator();

    CPU cpu;
    init_cpu(&cpu, SCHED_RR);

    add_process_to_cpu(&cpu, "nginx",  0, 10, 2);
    add_process_to_cpu(&cpu, "mysql",  0,  6, 1);
    add_process_to_cpu(&cpu, "redis",  1,  4, 1);
    add_process_to_cpu(&cpu, "python", 2,  8, 3);
    add_process_to_cpu(&cpu, "node",   3,  3, 2);
    add_process_to_cpu(&cpu, "cron",   5,  2, 4);

    run_simulation(&cpu);
    print_statistics(&cpu);
    print_gantt_chart(&cpu);
    cleanup_cpu(&cpu);
}

/* ==================== 主函数 ==================== */

int main(void) {
    printf("\n");
    print_separator();
    printf("       处理器管理（进程调度）模拟器 Demo\n");
    printf("       Process Management & CPU Scheduling\n");
    print_separator();

    test_fcfs();
    test_sjf();
    test_rr();
    test_priority();
    test_multi_rr();

    printf("\n");
    print_separator();
    printf("  所有测试完成！\n");
    print_separator();
    printf("\n");

    return 0;
}
