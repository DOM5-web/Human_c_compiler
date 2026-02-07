#ifndef VIBE_IO_H
#define VIBE_IO_H
#include <stdio.h>
#define vibe_print(...) printf(__VA_ARGS__)
#define vibe_error(...) fprintf(stderr, __VA_ARGS__)
#endif
