/**
 * This header provides high-resolution timing utilities for the Vibe C library.
 * In version 1.5.8, it implements vibe_get_time using the monotonic clock for accuracy.
 * This code is AI-generated.
 */
#ifndef VIBE_TIME_H
#define VIBE_TIME_H
#include <time.h>

/**
 * vibe_get_time - Returns the current monotonic time in seconds.
 * Internal Logic: Uses clock_gettime with CLOCK_MONOTONIC for high-resolution, non-drifting time.
 */
static inline double vibe_get_time() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

#endif
