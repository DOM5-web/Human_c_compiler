/**
 * This test verifies the security hardening of the thread pool implementation.
 * It checks the maximum thread limit and the rejection of jobs during shutdown.
 * This code is AI-generated.
 */
#include "../vibe/include/vibe_thread_pool.h"
#include "../vibe/include/vibe_test.h"
#include <unistd.h>

void empty_job(void* arg) {
    (void)arg;
}

int main() {
    printf("Starting thread pool security tests...\n");

    // Test 1: Thread limit
    vibe_thread_pool_t* oversized_pool = vibe_thread_pool_create(1025);
    VIBE_ASSERT(oversized_pool == NULL);
    if (oversized_pool) vibe_thread_pool_destroy(oversized_pool);

    // Test 2: Reasonable limit
    vibe_thread_pool_t* pool = vibe_thread_pool_create(4);
    VIBE_ASSERT(pool != NULL);

    // Test 3: Shutdown rejection
    pthread_mutex_lock(&(pool->lock));
    pool->shutdown = true; // Manually trigger shutdown for testing rejection
    pthread_mutex_unlock(&(pool->lock));

    vibe_thread_pool_add_job(pool, empty_job, NULL);
    VIBE_ASSERT(pool->queue_size == 0); // Job should have been rejected and freed

    // Test 4: Queue limit
    pthread_mutex_lock(&(pool->lock));
    pool->shutdown = false; // Re-enable for this test
    pool->max_queue_size = 2; // Set a small limit
    pthread_mutex_unlock(&(pool->lock));

    vibe_thread_pool_add_job(pool, empty_job, NULL);
    vibe_thread_pool_add_job(pool, empty_job, NULL);
    VIBE_ASSERT(pool->queue_size == 2);

    vibe_thread_pool_add_job(pool, empty_job, NULL); // Should be rejected
    VIBE_ASSERT(pool->queue_size == 2);

    // Cleanup (note: destroy expects threads to be joinable, but here they are still running)
    // To safely destroy after our manual shutdown trigger, we need to signal workers
    pthread_mutex_lock(&(pool->lock));
    pthread_cond_broadcast(&(pool->notify));
    pthread_mutex_unlock(&(pool->lock));

    vibe_thread_pool_destroy(pool);

    VIBE_TEST_SUMMARY();
}
