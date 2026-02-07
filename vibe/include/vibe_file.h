#ifndef VIBE_FILE_H
#define VIBE_FILE_H
#include <stdio.h>
#include <stdlib.h>
static inline char* vibe_read_file(const char* filename) {
    FILE* f = fopen(filename, "rb");
    if (!f) return NULL;
    fseek(f, 0, SEEK_END);
    long len = ftell(f);
    fseek(f, 0, SEEK_SET);
    char* data = (char*)malloc(len + 1);
    fread(data, 1, len, f);
    data[len] = '\0';
    fclose(f);
    return data;
}
#endif
