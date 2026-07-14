// 对于热点结构体，一个结构体刚好占一个 Cache Line。

#include <stdio.h>

struct Data {
    int a;
    int b;
    int c;
    int d;
};

struct AlignData {
    int value;
    char padding[60];
};

int main() {
    printf(
        "normal size=%ld\n",
        sizeof(struct Data)
    );

    printf(
        "align size=%ld\n",
        sizeof(struct AlignData)
    );

    return 0;
}