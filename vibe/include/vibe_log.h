#ifndef VIBE_LOG_H
#define VIBE_LOG_H
#include <stdio.h>
#define vibe_log_info(...)  printf("[INFO] " __VA_ARGS__) // nosec
#define vibe_log_warn(...)  printf("[WARN] " __VA_ARGS__) // nosec
#define vibe_log_error(...) fprintf(stderr, "[ERROR] " __VA_ARGS__) // nosec
#endif
