模拟架构

                 CPU线程
                    |
                    |
            创建/管理DMA Descriptor
                    |
                    ↓

          DMA Descriptor Ring

+---------+    +---------+    +---------+
| Desc 0  | -> | Desc 1  | -> | Desc 2  |
+---------+    +---------+    +---------+

                    |
                    |
                    ↓

              DMA线程

        自动读取Descriptor

                    |
                    ↓

              数据搬运

                    |
                    ↓

              更新状态

                    |
                    ↓

             DMA中断通知CPU

这里使用：
pthread 模拟 CPU线程和DMA硬件线程
mutex 模拟硬件资源竞争
condition variable 模拟 DMA 中断
Descriptor Ring 模拟网卡 RX/TX 描述符