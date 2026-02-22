#ifndef VIBE_BENCH_H
#define VIBE_BENCH_H
#include "vibe_time.h"
#include <stdio.h>
#define VIBE_BENCHMARK(name, block) do {     double start = vibe_get_time();     block;     double end = vibe_get_time();     printf("Benchmark '%s': %f seconds\n", name, end - start); /* nosec */ } while(0)
#endif
