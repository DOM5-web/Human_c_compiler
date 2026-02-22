#include "../vibe/include/vibe_thread_pool.h"
#include <stdio.h>
#include <unistd.h>

void sample_job(void* arg) {
    int id = *(int*)arg;
    printf("Job %d started\n", id); // nosec
    usleep(100000); // 100ms
    printf("Job %d finished\n", id); // nosec
}

int main() {
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
    sleep(2);

    // Note: The current thread pool implementation doesn't have a shutdown/free function
    // that waits for all jobs, but we can at least verify it runs.
    // In a real scenario, we'd add a vibe_thread_pool_destroy.

    printf("Functional test complete.\n"); // nosec
    return 0;
}
