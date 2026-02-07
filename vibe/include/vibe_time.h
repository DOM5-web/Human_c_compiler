#ifndef VIBE_TIME_H
#define VIBE_TIME_H
#include <time.h>
static inline double vibe_get_time() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}
#endif
