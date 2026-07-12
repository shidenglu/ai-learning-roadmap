# 矩阵分块

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 1024
#define BLOCK 32

double A[N][N];
double B[N][N];
double C[N][N];


// 普通矩阵乘法
void matrix_normal(){
    for(int i = 0; i < N; i++) {
        for(int j = 0; j < N; j++) {
            C[i][j] = 0;
            for(int k = 0; k < N; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}



// Cache Blocking
void matrix_block(){
    for(int ii = 0; ii < N; ii += BLOCK){
        for(int jj = 0; jj < N; jj += BLOCK) {
            for(int kk = 0; kk < N; kk += BLOCK) {
                for(int i = ii; i < ii + BLOCK; i++) {
                    for(int j = jj; j < jj + BLOCK; j++) {
                        for(int k = kk ;k < kk + BLOCK; k++) {
                            C[i][j] += A[i][k] * B[k][j];
                        }
                    }
                }
            }
        }
    }
}



int main() {
    for(int i = 0; i < N; i++) {
        for(int j=0; j < N; j++) {
            A[i][j] = 1;
            B[i][j] = 1;
            C[i][j] = 0;

        }
    }

    clock_t start;
    start=clock();
    matrix_normal();

    printf(
        "normal=%lf s\n",
        (double)(clock()-start)
        /
        CLOCKS_PER_SEC
    );

    start=clock();
    matrix_block();
    printf(
        "block=%lf s\n",
        (double)(clock()-start)
        /
        CLOCKS_PER_SEC
    );
}