#ifndef VIBE_MEM_H
#define VIBE_MEM_H
#include <stdlib.h>
#define vibe_alloc(sz) malloc(sz)
#define vibe_free(p) free(p)

/**
 * vibe_secure_memzero - Securely clear memory to avoid compiler optimization
 * @p: Pointer to memory to clear
 * @len: Length of memory to clear
 */
static inline void vibe_secure_memzero(void* p, size_t len) {
    if (!p) return;
    volatile unsigned char* ptr = (volatile unsigned char*)p;
    while (len--) {
        *ptr++ = 0;
    }
}

#endif
