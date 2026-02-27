/**
 * This header provides a simple wrapper around the POSIX threads (pthreads) library.
 * In version 1.5.6, it continues to provide basic macros for thread creation and joining.
 * This code is AI-generated.
 */
#ifndef VIBE_THREAD_H
#define VIBE_THREAD_H
#include <pthread.h>

// Internal Logic: Re-define pthread_t for consistency within the Vibe namespace.
typedef pthread_t vibe_thread_t;

// Internal Logic: Macros for basic thread lifecycle management.
#define vibe_thread_create(t, f, a) pthread_create(t, NULL, f, a)
#define vibe_thread_join(t) pthread_join(t, NULL)

#endif
