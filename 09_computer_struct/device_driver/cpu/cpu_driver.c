#include <stdio.h>
#include "cpu_driver.h"

/* CPU 初始化 */
int CPU_Init(CPU_Device *cpu)
{
    if (cpu == NULL)
        return -1;

    cpu->core_id = 0;
    cpu->frequency_mhz = 1000;
    cpu->state = CPU_STATE_IDLE;

    printf("[CPU] Initialize Core %u\n",
           cpu->core_id);

    return 0;
}

/* 启动 CPU */
int CPU_Start(CPU_Device *cpu)
{
    if (cpu == NULL)
        return -1;

    cpu->state = CPU_STATE_RUNNING;

    printf("[CPU] Core %u Started\n",
           cpu->core_id);

    return 0;
}

/* 停止 CPU */
int CPU_Stop(CPU_Device *cpu)
{
    if (cpu == NULL)
        return -1;

    cpu->state = CPU_STATE_IDLE;

    printf("[CPU] Core %u Stopped\n",
           cpu->core_id);

    return 0;
}

/* 设置 CPU 频率 */
int CPU_SetFrequency(CPU_Device *cpu,
                     uint32_t frequency_mhz)
{
    if (cpu == NULL || frequency_mhz == 0)
        return -1;

    cpu->frequency_mhz = frequency_mhz;

    printf("[CPU] Frequency: %u MHz\n",
           frequency_mhz);

    return 0;
}

/* 获取 CPU 状态 */
void CPU_GetStatus(CPU_Device *cpu)
{
    if (cpu == NULL)
        return;

    printf("\n========== CPU STATUS ==========\n");

    printf("Core ID   : %u\n", cpu->core_id);

    printf("Frequency : %u MHz\n",
           cpu->frequency_mhz);

    switch (cpu->state) {
    case CPU_STATE_OFF:
        printf("State     : OFF\n");
        break;

    case CPU_STATE_IDLE:
        printf("State     : IDLE\n");
        break;

    case CPU_STATE_RUNNING:
        printf("State     : RUNNING\n");
        break;

    default:
        printf("State     : UNKNOWN\n");
        break;
    }

    printf("================================\n");
}

/* Demo */
int main(void)
{
    CPU_Device cpu;

    /* 1. 初始化 CPU */
    CPU_Init(&cpu);

    /* 2. 设置 CPU 频率 */
    CPU_SetFrequency(&cpu, 2400);

    /* 3. 启动 CPU */
    CPU_Start(&cpu);

    /* 4. 获取 CPU 状态 */
    CPU_GetStatus(&cpu);

    /* 5. 停止 CPU */
    CPU_Stop(&cpu);

    /* 6. 再次获取 CPU 状态 */
    CPU_GetStatus(&cpu);

    return 0;
}