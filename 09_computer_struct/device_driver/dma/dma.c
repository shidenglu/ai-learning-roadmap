#include <stdio.h>
#include <string.h>

/*
 * DMA Descriptor状态
 */
typedef enum {
    DMA_IDLE = 0,
    DMA_BUSY,
    DMA_DONE,
    DMA_ERROR
} DMA_STATUS;


/*
 * DMA Descriptor
 *
 * 模拟硬件中的描述符
 */
typedef struct DMA_Descriptor {
    unsigned char *src;      // 源地址
    unsigned char *dst;      // 目的地址
    unsigned int length;     // 数据长度
    DMA_STATUS status;       // 状态
    int own;                 // 0 CPU拥有
                             // 1 DMA拥有
} DMA_Descriptor;

/*
 * 模拟DMA控制器
 */
typedef struct {
    DMA_Descriptor *desc;

} DMA_Controller;


/*
 * DMA执行函数
 *
 * 模拟DMA硬件工作
 */
void dma_transfer(DMA_Controller *dma) {

    DMA_Descriptor *desc = dma->desc;

    /*
     * 检查Descriptor是否属于DMA
     */
    if (desc->own != 1) {
        printf("DMA: Descriptor not owned by DMA\n");
        return;
    }

    printf("DMA start transfer...\n");

    desc->status = DMA_BUSY;

    /*
     * DMA真正搬数据
     *
     * 硬件完成：
     *
     * 外设 ---> RAM
     *
     */
    memcpy(
        desc->dst,
        desc->src,
        desc->length
    );

    printf("DMA copy %d bytes\n",
            desc->length);

    /*
     * 更新Descriptor状态
     */

    desc->status = DMA_DONE;

    /*
     * 归还CPU
     */
    desc->own = 0;

    printf("DMA transfer complete\n");

}


/*
 * 模拟DMA中断
 */
void dma_interrupt(DMA_Controller *dma) {

    DMA_Descriptor *desc=dma->desc;

    if(desc->status == DMA_DONE) {
        printf("CPU: DMA interrupt received\n");
        printf("CPU: Data transfer finished\n");
    }
}

int main() {

    /*
     * 模拟外设数据
     *
     * 比如：
     *
     * UART FIFO
     *
     * Ethernet RX FIFO
     *
     */
    unsigned char peripheral_buffer[] =
    {
        'H',
        'e',
        'l',
        'l',
        'o',
        ' ',
        'D',
        'M',
        'A'
    };

    /*
     * 模拟RAM
     *
     * DMA目标地址
     */
    unsigned char memory_buffer[32]={0};

    /*
     * CPU创建Descriptor
     */
    DMA_Descriptor descriptor;
    descriptor.src = peripheral_buffer;
    descriptor.dst = memory_buffer;
    descriptor.length = sizeof(peripheral_buffer);

    descriptor.status =
        DMA_IDLE;

    /*
     * 交给DMA
     */
    descriptor.own = 1;

    /*
     * 创建DMA控制器
     */
    DMA_Controller dma;


    dma.desc=&descriptor;

    printf("CPU: Configure DMA\n");

    /*
     * 启动DMA
     */
    dma_transfer(&dma);

    /*
     * DMA完成产生中断
     */
    dma_interrupt(&dma);

    printf("\n");

    printf("Memory data:\n");

    printf("%s\n",
           memory_buffer);

    return 0;
}