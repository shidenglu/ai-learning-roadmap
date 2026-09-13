#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>

#define DMA_DESC_NUM 4
#define BUFFER_SIZE 128

/*
 * DMA Descriptor状态
 */
typedef enum {
    DESC_FREE = 0,
    DESC_READY,
    DESC_BUSY,
    DESC_DONE
} DESC_STATUS;

/*
 * DMA Descriptor
 *
 * 模拟真实硬件Descriptor
 */
typedef struct {
    unsigned char *src;
    unsigned char *dst;
    int length;
    DESC_STATUS status;

    /*
     * OWN位
     *
     * 0 CPU拥有
     *
     * 1 DMA拥有
     */
    int own;
} DMA_Descriptor;

/*
 * DMA Ring
 */
typedef struct {
    DMA_Descriptor desc[DMA_DESC_NUM];
    int dma_index;
    pthread_mutex_t lock;
    pthread_cond_t irq;
} DMA_Ring;

DMA_Ring dma_ring;

/*
 * 模拟DMA硬件线程
 *
 * 类似：
 *
 * Ethernet DMA Engine
 */
void *dma_thread(void *arg) {
    while(1) {
        pthread_mutex_lock(
            &dma_ring.lock
        );

        DMA_Descriptor *desc =
            &dma_ring.desc[dma_ring.dma_index];

        /*
         * 检查Descriptor是否属于DMA
         */
        if(desc->own == 1 && desc->status == DESC_READY) {
            printf(
              "\nDMA: process descriptor %d\n",
              dma_ring.dma_index
            );

            desc->status = DESC_BUSY;

            pthread_mutex_unlock(
                &dma_ring.lock
            );

            /*
             * 模拟DMA搬数据时间
             */
            usleep(500000);

            memcpy(
                desc->dst,
                desc->src,
                desc->length
            );

            pthread_mutex_lock(
                &dma_ring.lock
            );

            desc->status =
                DESC_DONE;

            /*
             * 归还CPU
             */
            desc->own=0;

            printf(
              "DMA: descriptor %d done\n",
              dma_ring.dma_index
            );

            /*
             * DMA中断
             */
            pthread_cond_signal(
                &dma_ring.irq
            );

            dma_ring.dma_index++;

            if(dma_ring.dma_index >= DMA_DESC_NUM) {
                dma_ring.dma_index=0;
            }

        }

        pthread_mutex_unlock(
            &dma_ring.lock
        );

        usleep(100000);
    }

    return NULL;
}

/*
 * CPU线程
 *
 * 模拟驱动程序
 */
void *cpu_thread(void *arg) {

    for (int i = 0; i < DMA_DESC_NUM; i++) {
        pthread_mutex_lock(
            &dma_ring.lock
        );

        DMA_Descriptor *desc =
            &dma_ring.desc[i];

        /*
         * CPU填写Descriptor
         */
        sprintf(
            (char*)desc->src,
            "Packet-%d from CPU",
            i
        );

        desc->dst[0]=0;
        desc->length = strlen((char*)desc->src)+1;
        desc->status = DESC_READY;

        /*
         * 交给DMA
         */
        desc->own=1;

        printf(
            "CPU: submit descriptor %d\n",
            i
        );

        pthread_mutex_unlock(
            &dma_ring.lock
        );

        sleep(1);
    }

    /*
     * 等待DMA完成
     */
    while(1) {
        pthread_mutex_lock(
            &dma_ring.lock
        );

        pthread_cond_wait(
            &dma_ring.irq,
            &dma_ring.lock
        );

        printf("\nCPU IRQ:\n");

        for(int i=  0; i < DMA_DESC_NUM; i++){
            if(dma_ring.desc[i].status == DESC_DONE) {
                printf(
                 "Descriptor %d completed: %s\n",
                 i,
                 dma_ring.desc[i].dst
                );
            }
        }

        pthread_mutex_unlock(
            &dma_ring.lock
        );

    }
    return NULL;
}


int main() {
    pthread_t cpu;
    pthread_t dma;

    /*
     * 初始化Ring
     */
    pthread_mutex_init(
        &dma_ring.lock,
        NULL
    );

    pthread_cond_init(
        &dma_ring.irq,
        NULL
    );

    for(int i = 0; i < DMA_DESC_NUM; i++) {
        dma_ring.desc[i].src =
            malloc(BUFFER_SIZE);

        dma_ring.desc[i].dst =
            malloc(BUFFER_SIZE);

        dma_ring.desc[i].status =
            DESC_FREE;

        dma_ring.desc[i].own=0;
    }

    dma_ring.dma_index=0;

    /*
     * 创建线程
     */
    pthread_create(
        &dma,
        NULL,
        dma_thread,
        NULL
    );

    pthread_create(
        &cpu,
        NULL,
        cpu_thread,
        NULL
    );

    pthread_join(cpu,NULL);
    pthread_join(dma,NULL);
    return 0;
}