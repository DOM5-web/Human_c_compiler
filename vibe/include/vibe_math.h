/**
 * This header provides common math constants and helper macros for the Vibe C library.
 * In version 1.5.6, it continues to provide PI and E constants, as well as min/max macros.
 * This code is AI-generated.
 */
#ifndef VIBE_MATH_H
#define VIBE_MATH_H
#include <math.h>

// Internal Logic: Define mathematical constants with double precision.
#define VIBE_PI 3.14159265358979323846
#define VIBE_E  2.71828182845904523536

// Internal Logic: Provide simple min/max macros. Note that these may evaluate arguments twice.
#define vibe_max(a,b) ((a) > (b) ? (a) : (b))
#define vibe_min(a,b) ((a) < (b) ? (a) : (b))

#endif
