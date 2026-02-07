#ifndef VIBE_UI_H
#define VIBE_UI_H
#include "vibe_color.h"
#include <stdio.h>
static inline void vibe_ui_header(const char* title) {
    printf("%s=== %s ===%s\n", VIBE_BLUE, title, VIBE_RESET);
}
#endif
