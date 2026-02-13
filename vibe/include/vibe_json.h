#ifndef VIBE_JSON_H
#define VIBE_JSON_H

#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stdio.h>

typedef enum {
    VIBE_JSON_NULL,
    VIBE_JSON_BOOL,
    VIBE_JSON_NUMBER,
    VIBE_JSON_STRING,
    VIBE_JSON_ARRAY,
    VIBE_JSON_OBJECT
} vibe_json_type_t;

typedef struct vibe_json_value {
    vibe_json_type_t type;
    union {
        bool boolean;
        double number;
        char* string;
        struct {
            struct vibe_json_value** elements;
            size_t count;
        } array;
        struct {
            char** keys;
            struct vibe_json_value** values;
            size_t count;
        } object;
    } value;
} vibe_json_value_t;

static inline vibe_json_value_t* vibe_json_new_string(const char* s) {
    vibe_json_value_t* v = (vibe_json_value_t*)malloc(sizeof(vibe_json_value_t));
    if (!v) return NULL;
    v->type = VIBE_JSON_STRING;
    v->value.string = strdup(s);
    if (!v->value.string) {
        free(v);
        return NULL;
    }
    return v;
}

static inline void vibe_json_free(vibe_json_value_t* v) {
    if (!v) return;
    if (v->type == VIBE_JSON_STRING) {
        free(v->value.string);
    } else if (v->type == VIBE_JSON_ARRAY) {
        for (size_t i = 0; i < v->value.array.count; i++) {
            vibe_json_free(v->value.array.elements[i]);
        }
        free(v->value.array.elements);
    } else if (v->type == VIBE_JSON_OBJECT) {
        for (size_t i = 0; i < v->value.object.count; i++) {
            free(v->value.object.keys[i]);
            vibe_json_free(v->value.object.values[i]);
        }
        free(v->value.object.keys);
        free(v->value.object.values);
    }
    free(v);
}

static inline void _vibe_json_print_escaped(const char* s) {
    printf("\"");
    for (const char* p = s; *p; p++) {
        if (*p == '\"' || *p == '\\') putchar('\\');
        putchar(*p);
    }
    printf("\"");
}

static inline void vibe_json_print(vibe_json_value_t* v) {
    if (!v) { printf("null"); return; }
    switch(v->type) {
        case VIBE_JSON_NULL: printf("null"); break;
        case VIBE_JSON_BOOL: printf(v->value.boolean ? "true" : "false"); break;
        case VIBE_JSON_NUMBER: printf("%g", v->value.number); break;
        case VIBE_JSON_STRING: _vibe_json_print_escaped(v->value.string); break;
        case VIBE_JSON_ARRAY:
            printf("[");
            for (size_t i = 0; i < v->value.array.count; i++) {
                vibe_json_print(v->value.array.elements[i]);
                if (i < v->value.array.count - 1) printf(",");
            }
            printf("]");
            break;
        case VIBE_JSON_OBJECT:
            printf("{");
            for (size_t i = 0; i < v->value.object.count; i++) {
                _vibe_json_print_escaped(v->value.object.keys[i]);
                printf(":");
                vibe_json_print(v->value.object.values[i]);
                if (i < v->value.object.count - 1) printf(",");
            }
            printf("}");
            break;
        default: printf("???");
    }
}

#endif
