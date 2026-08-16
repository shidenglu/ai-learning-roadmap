#include "../include/stats.h"

void print_separator(void) {
    printf("============================================================"
           "========================\n");
}

void print_thin_separator(void) {
    printf("------------------------------------------------------------"
           "------------------------\n");
}

void print_statistics(CPU *cpu) {
    printf("\n");
    print_separator();
    printf("  调度统计报告 | 算法: %s\n", algorithm_to_string(cpu->algorithm));
    print_separator();

    printf("\n  %-6s %-12s %-8s %-8s %-8s %-10s %-10s %-8s\n",
           "PID", "名称", "到达", "服务", "完成", "周转", "等待", "响应");
    print_thin_separator();

    float total_turnaround = 0;
    float total_wait = 0;
    float total_response = 0;

    for (int i = 0; i < cpu->process_count; i++) {
        PCB *p = cpu->process_table[i];
        printf("  %-6d %-12s %-8d %-8d %-8d %-10d %-10d %-8d\n",
               p->pid, p->name, p->arrival_time, p->burst_time,
               p->finish_time, p->turnaround_time, p->wait_time,
               p->response_time);

        total_turnaround += p->turnaround_time;
        total_wait += p->wait_time;
        total_response += (p->response_time >= 0) ? p->response_time : 0;
    }

    print_thin_separator();
    printf("  平均周转时间: %.2f\n", total_turnaround / cpu->process_count);
    printf("  平均等待时间: %.2f\n", total_wait / cpu->process_count);
    printf("  平均响应时间: %.2f\n", total_response / cpu->process_count);
    printf("  总完成时间:   %d\n", cpu->total_time);
    print_separator();
}

void print_gantt_chart(CPU *cpu) {
    printf("\n  甘特图:\n  ");

    // 打印时间刻度
    for (int t = 0; t <= cpu->total_time; t++) {
        printf("%-4d", t);
    }
    printf("\n  ");

    // 打印进程块
    for (int t = 0; t < cpu->total_time; t++) {
        char found = 0;
        for (int i = 0; i < cpu->process_count; i++) {
            PCB *p = cpu->process_table[i];
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
