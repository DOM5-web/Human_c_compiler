#ifndef VIBE_TEST_H
#define VIBE_TEST_H
#include <stdio.h>
#define VIBE_ASSERT(cond) do {     if (!(cond)) {         printf("[FAIL] Assertion failed: %s at %s:%d\n", #cond, __FILE__, __LINE__);     } else {         printf("[PASS] %s\n", #cond);     } } while(0)
#endif
