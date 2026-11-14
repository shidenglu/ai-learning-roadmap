#ifndef CPU_DRIVER_H
#define CPU_DRIVER_H

#include <stdint.h>

/* CPU 状态 */
typedef enum {
    CPU_STATE_OFF = 0,
    CPU_STATE_IDLE,
    CPU_STATE_RUNNING
} CPU_State;

/* CPU 设备结构体 */
typedef struct {
    uint32_t core_id;
    uint32_t frequency_mhz;
    CPU_State state;
} CPU_Device;

/* CPU 驱动接口 */
int CPU_Init(CPU_Device *cpu);

int CPU_Start(CPU_Device *cpu);

int CPU_Stop(CPU_Device *cpu);

int CPU_SetFrequency(CPU_Device *cpu,
                     uint32_t frequency_mhz);

void CPU_GetStatus(CPU_Device *cpu);

#endif