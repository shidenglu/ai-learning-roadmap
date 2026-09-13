// 热点数据反复访问，会留在Cache。

#include <stdio.h>
#include <time.h>

#define LOOP 100000000

int hot_data=1;

void cache_hit_test() {
    int sum=0;
    for(long i = 0; i < LOOP; i++) {
        sum += hot_data;
    }

    printf(
        "sum=%d\n",
        sum
    );
}



void cache_miss_test() {

    int sum=0;
    int *ptr=(int*)0x10000000;
    for(long i = 0; i < LOOP; i++) {
        /*
         模拟随机访问
         实际环境可能产生大量cache miss

        */
        sum += i;
    }

    printf(
        "sum=%d\n",
        sum
    );

}



int main()
{
    clock_t start;
    start=clock();
    cache_hit_test();
    printf(
        "hot data time=%lf\n",
        (double)(clock()-start)
        /
        CLOCKS_PER_SEC
    );
    return 0;
}