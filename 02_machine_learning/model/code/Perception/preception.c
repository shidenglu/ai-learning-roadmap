#include <stdio.h>

#define EPOCHS 20

int step(float z) {
    return z >= 0 ? 1 : 0;
}

int main() {
    /* AND训练数据 */
    float X[4][2] =
    {
        {0,0},
        {0,1},
        {1,0},
        {1,1}
    };

    int Y[4] =
    {
        0,
        0,
        0,
        1
    };

    /* 初始化参数 */
    float w1 = 0.0f;
    float w2 = 0.0f;
    float b  = 0.0f;

    float lr = 0.1f;
    printf("开始训练...\n\n");

    for(int epoch = 0; epoch < EPOCHS; epoch++) {
        int error_count = 0;
        for(int i = 0; i < 4; i++) {
            float x1 = X[i][0];
            float x2 = X[i][1];

            int target = Y[i];

            /* 前向传播 */
            float z = w1 * x1 +
                      w2 * x2 +
                      b;

            int pred = step(z);
            /* 误差 */

            int error = target - pred;
            if(error != 0) {
                error_count++;
            }

            /* 更新参数 */
            w1 += lr * error * x1;
            w2 += lr * error * x2;
            b  += lr * error;
        }

        printf(
            "epoch=%2d  w1=%6.3f  w2=%6.3f  b=%6.3f  error=%d\n",
            epoch + 1,
            w1,
            w2,
            b,
            error_count
        );

        if(error_count == 0) {
            break;
        }
    }

    printf("\n训练完成\n");

    printf(
        "最终参数:\n"
        "w1 = %.3f\n"
        "w2 = %.3f\n"
        "b  = %.3f\n\n",
        w1,
        w2,
        b
    );

    printf("测试结果:\n");

    for(int i = 0; i < 4; i++) {
        float x1 = X[i][0];
        float x2 = X[i][1];

        float z =
            w1*x1 +
            w2*x2 +
            b;

        int pred = step(z);

        printf(
            "%.0f %.0f -> %d\n",
            x1,
            x2,
            pred
        );
    }

    return 0;
}