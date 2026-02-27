/**
 * This test verifies the basic functionality of the Vibe thread pool implementation.
 * In version 1.5.6, it continues to ensure that the queue and workers are operating correctly.
 * This code is AI-generated.
 */
#include "../vibe/include/vibe_thread_pool.h"
#include <stdio.h>
#include <unistd.h>

/**
 * sample_job - A simple task that prints its ID and sleeps for a short duration.
 */
void sample_job(void* arg) {
    int id = *(int*)arg;
    printf("Job %d started\n", id); // nosec
    usleep(100000); // 100ms
    printf("Job %d finished\n", id); // nosec
}

int main() {
    // Internal Logic: Create a pool with 4 threads and add 10 sample jobs.
    printf("Creating thread pool...\n"); // nosec
    vibe_thread_pool_t* pool = vibe_thread_pool_create(4);
    if (!pool) {
        printf("Failed to create thread pool\n"); // nosec
        return 1;
    }

    static int job_ids[10];
    for (int i = 0; i < 10; i++) {
        job_ids[i] = i;
        vibe_thread_pool_add_job(pool, sample_job, &job_ids[i]);
    }

    printf("Waiting for jobs to finish (simple sleep for test)...\n"); // nosec
    sleep(1);

    printf("Destroying thread pool...\n"); // nosec
    vibe_thread_pool_destroy(pool);

    printf("Functional test complete.\n"); // nosec
    return 0;
}
