/**
 * This header provides simple terminal User Interface (UI) helpers for the Vibe C library.
 * In version 1.5.6, it uses Vibe color constants to format and print headers to stdout.
 * This code is AI-generated.
 */
#ifndef VIBE_UI_H
#define VIBE_UI_H
#include "vibe_color.h"
#include <stdio.h>

/**
 * vibe_ui_header - Prints a colorized section header to the terminal.
 * Internal Logic: Wraps the title in blue ANSI escape codes and consistent formatting markers.
 */
static inline void vibe_ui_header(const char* title) {
    if (!title) return;
    printf("%s=== %s ===%s\n", VIBE_BLUE, title, VIBE_RESET); // nosec
}

#endif
