#ifndef VIBE_THREAD_POOL_H
#define VIBE_THREAD_POOL_H

#include <pthread.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct vibe_job {
    void (*function)(void* arg);
    void* arg;
    struct vibe_job* next;
} vibe_job_t;

typedef struct {
    pthread_mutex_t lock;
    pthread_cond_t notify;
    pthread_t* threads;
    vibe_job_t* queue_head;
    int thread_count;
    int queue_size;
    bool shutdown;
} vibe_thread_pool_t;

static void* vibe_worker(void* thread_pool) {
    vibe_thread_pool_t* pool = (vibe_thread_pool_t*)thread_pool;
    while (true) {
        pthread_mutex_lock(&(pool->lock));
        while (pool->queue_size == 0 && !pool->shutdown) {
            pthread_cond_wait(&(pool->notify), &(pool->lock));
        }
        if (pool->shutdown) {
            pthread_mutex_unlock(&(pool->lock));
            pthread_exit(NULL);
        }
        vibe_job_t* job = pool->queue_head;
        pool->queue_head = job->next;
        pool->queue_size--;
        pthread_mutex_unlock(&(pool->lock));
        (*(job->function))(job->arg);
        free(job);
    }
    return NULL;
}

static inline vibe_thread_pool_t* vibe_thread_pool_create(int num_threads) {
    vibe_thread_pool_t* pool = (vibe_thread_pool_t*)malloc(sizeof(vibe_thread_pool_t));
    pool->thread_count = num_threads;
    pool->queue_size = 0;
    pool->queue_head = NULL;
    pool->shutdown = false;
    pthread_mutex_init(&(pool->lock), NULL);
    pthread_cond_init(&(pool->notify), NULL);
    pool->threads = (pthread_t*)malloc(sizeof(pthread_t) * num_threads);
    for (int i = 0; i < num_threads; i++) {
        pthread_create(&(pool->threads[i]), NULL, vibe_worker, (void*)pool);
    }
    return pool;
}

static inline void vibe_thread_pool_add_job(vibe_thread_pool_t* pool, void (*function)(void*), void* arg) {
    vibe_job_t* job = (vibe_job_t*)malloc(sizeof(vibe_job_t));
    job->function = function;
    job->arg = arg;
    job->next = NULL;
    pthread_mutex_lock(&(pool->lock));
    if (pool->queue_head == NULL) {
        pool->queue_head = job;
    } else {
        vibe_job_t* last = pool->queue_head;
        while (last->next) last = last->next;
        last->next = job;
    }
    pool->queue_size++;
    pthread_cond_signal(&(pool->notify));
    pthread_mutex_unlock(&(pool->lock));
}

#endif
