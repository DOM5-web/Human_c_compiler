#ifndef VIBE_IO_H
#define VIBE_IO_H
#include <stdio.h>
#define vibe_print(fmt, ...) printf("" fmt, ##__VA_ARGS__)
#define vibe_error(fmt, ...) fprintf(stderr, "" fmt, ##__VA_ARGS__)
#endif
