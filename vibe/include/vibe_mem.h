#ifndef VIBE_MEM_H
#define VIBE_MEM_H
#include <stdlib.h>
#define vibe_alloc(sz) malloc(sz)
#define vibe_free(p) free(p)
#endif
