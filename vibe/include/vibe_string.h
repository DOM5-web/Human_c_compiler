#ifndef VIBE_STRING_H
#define VIBE_STRING_H
#include <string.h>
#include <stdbool.h>
static inline bool vibe_str_eq(const char* s1, const char* s2) {
    return strcmp(s1, s2) == 0;
}
#endif
