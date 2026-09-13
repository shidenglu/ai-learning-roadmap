#include "../include/queue.h"

void init_ready_queue(ReadyQueue *queue) {
    queue->head = NULL;
    queue->tail = NULL;
    queue->count = 0;
}

void enqueue_sorted(ReadyQueue *queue, PCB *pcb, SchedAlgorithm alg) {
    pcb->state = STATE_READY;
    pcb->next = NULL;

    if (queue->count == 0) {
        queue->head = pcb;
        queue->tail = pcb;
        queue->count++;
        return;
    }

    if (alg == SCHED_SJF) {
        if (pcb->remaining_time < queue->head->remaining_time) {
            pcb->next = queue->head;
            queue->head = pcb;
            queue->count++;
            return;
        }
        PCB *curr = queue->head;
        while (curr->next && curr->next->remaining_time <= pcb->remaining_time) {
            curr = curr->next;
        }
        pcb->next = curr->next;
        curr->next = pcb;
        if (curr == queue->tail) queue->tail = pcb;
        queue->count++;
    } else if (alg == SCHED_PRIORITY) {
        if (pcb->priority < queue->head->priority) {
            pcb->next = queue->head;
            queue->head = pcb;
            queue->count++;
            return;
        }
        PCB *curr = queue->head;
        while (curr->next && curr->next->priority <= pcb->priority) {
            curr = curr->next;
        }
        pcb->next = curr->next;
        curr->next = pcb;
        if (curr == queue->tail) queue->tail = pcb;
        queue->count++;
    } else {
        queue->tail->next = pcb;
        queue->tail = pcb;
        queue->count++;
    }
}

PCB* dequeue(ReadyQueue *queue) {
    if (queue->count == 0) return NULL;

    PCB *pcb = queue->head;
    queue->head = queue->head->next;
    if (queue->count == 1) queue->tail = NULL;
    pcb->next = NULL;
    queue->count--;
    return pcb;
}

void move_tail_to_head(ReadyQueue *queue) {
    if (queue->count <= 1) return;

    PCB *prev = queue->head;
    while (prev->next != queue->tail) {
        prev = prev->next;
    }

    PCB *tail_node = queue->tail;
    prev->next = NULL;
    queue->tail = prev;

    tail_node->next = queue->head;
    queue->head = tail_node;
}

void print_ready_queue(ReadyQueue *queue) {
    if (queue->count == 0) {
        printf("  [就绪队列为空]\n");
        return;
    }
    printf("  就绪队列 (%d个进程): ", queue->count);
    PCB *curr = queue->head;
    while (curr) {
        printf("P%d(%s)", curr->pid, curr->name);
        if (curr->next) printf(" -> ");
        curr = curr->next;
    }
    printf("\n");
}

void sort_queue_fcfs(ReadyQueue *queue) {
    if (queue->count <= 1) return;

    PCB *arr[MAX_READY_QUEUE];
    int n = 0;
    PCB *curr = queue->head;
    while (curr && n < MAX_READY_QUEUE) {
        arr[n++] = curr;
        curr = curr->next;
    }

    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (arr[j]->arrival_time > arr[j + 1]->arrival_time) {
                PCB *temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }

    queue->head = arr[0];
    for (int i = 0; i < n - 1; i++) {
        arr[i]->next = arr[i + 1];
    }
    arr[n - 1]->next = NULL;
    queue->tail = arr[n - 1];
}

void sort_queue_sjf(ReadyQueue *queue) {
    if (queue->count <= 1) return;

    PCB *arr[MAX_READY_QUEUE];
    int n = 0;
    PCB *curr = queue->head;
    while (curr && n < MAX_READY_QUEUE) {
        arr[n++] = curr;
        curr = curr->next;
    }

    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (arr[j]->burst_time > arr[j + 1]->burst_time) {
                PCB *temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }

    queue->head = arr[0];
    for (int i = 0; i < n - 1; i++) {
        arr[i]->next = arr[i + 1];
    }
    arr[n - 1]->next = NULL;
    queue->tail = arr[n - 1];
}

void sort_queue_priority(ReadyQueue *queue) {
    if (queue->count <= 1) return;

    PCB *arr[MAX_READY_QUEUE];
    int n = 0;
    PCB *curr = queue->head;
    while (curr && n < MAX_READY_QUEUE) {
        arr[n++] = curr;
        curr = curr->next;
    }

    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (arr[j]->priority > arr[j + 1]->priority) {
                PCB *temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }

    queue->head = arr[0];
    for (int i = 0; i < n - 1; i++) {
        arr[i]->next = arr[i + 1];
    }
    arr[n - 1]->next = NULL;
    queue->tail = arr[n - 1];
}
