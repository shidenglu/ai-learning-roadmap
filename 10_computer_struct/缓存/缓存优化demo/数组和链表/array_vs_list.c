// 数组访问效率比链表高

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 10000000

typedef struct Node {
    int value;
    struct Node *next;
} Node;

int main() {
    int *array;
    array= malloc(sizeof(int) * N);

    Node *head = NULL;

    for(int i = 0; i < N; i++) {
        array[i] = 1;

        Node *node = malloc(sizeof(Node));
        node->value=1;
        node->next=head;
        head=node;
    }

    long sum=0;

    clock_t start;

    start = clock();

    for(int i = 0; i < N; i++) {
        sum += array[i];
    }

    printf(
        "array time=%lf\n",
        (double)(clock()-start)
        /
        CLOCKS_PER_SEC
    );

    sum=0;
    start=clock();
    Node *p = head;

    while(p) {
        sum+=p->value;
        p=p->next;
    }

    printf(
        "list time=%lf\n",
        (double)(clock()-start)
        /
        CLOCKS_PER_SEC
    );

    return 0;
}