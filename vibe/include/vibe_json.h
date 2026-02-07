#ifndef VIBE_JSON_H
#define VIBE_JSON_H

#include <stdlib.h>
#include <string.h>

typedef enum {
    VIBE_JSON_NULL,
    VIBE_JSON_BOOL,
    VIBE_JSON_NUMBER,
    VIBE_JSON_STRING,
    VIBE_JSON_ARRAY,
    VIBE_JSON_OBJECT
} vibe_json_type_t;

typedef struct {
    vibe_json_type_t type;
    union {
        bool boolean;
        double number;
        char* string;
    } value;
} vibe_json_value_t;

// Placeholder functions for future implementation
static inline vibe_json_value_t* vibe_json_parse(const char* json_str) {
    (void)json_str;
    return NULL;
}

static inline void vibe_json_free(vibe_json_value_t* val) {
    (void)val;
}

#endif
