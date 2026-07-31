// 连续访问内存比跳跃访问快

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 5000

int matrix[N][N];

// 行访问
void row_access()
{
    long long sum = 0;
    for(int i = 0; i < N; i++) {
        for(int j = 0; j < N; j++) {
            sum += matrix[i][j];
        }
    }
    printf("row sum=%lld\n",sum);
}



// 列访问
void column_access()
{
    long long sum = 0;
    for(int j = 0; j < N; j++) {
        for(int i = 0; i < N; i++) {
            sum += matrix[i][j];
        }
    }


    printf("column sum = %lld\n",sum);
}



double get_time()
{
    return (double)clock()
        / CLOCKS_PER_SEC;
}



int main() {
    printf("init matrix...\n");
    for(int i = 0; i < N; i++) {
        for(int j = 0; j < N; j++)
        {
            matrix[i][j] = 1;
        }
    }
    double start;

    start = get_time();
    row_access();
    printf(
        "row time=%lf s\n",
        get_time() - start
    );

    start = get_time();
    column_access();
    printf(
        "column time = %lf s\n",
        get_time() - start
    );

    return 0;
}