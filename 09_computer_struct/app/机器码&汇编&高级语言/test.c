#include <stdio.h>


int add(int a, int b) {
    return a + b;
}


int main() {
    int x = 10;
    int y = 20;

    int result;

    result = add(x,y);

    if(result > 20)
    {
        result++;
    }

    printf("%d\n", result);

    return 0;
}