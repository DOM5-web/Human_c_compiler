#ifndef VIBE_THREAD_H
#define VIBE_THREAD_H
#include <pthread.h>
typedef pthread_t vibe_thread_t;
#define vibe_thread_create(t, f, a) pthread_create(t, NULL, f, a)
#define vibe_thread_join(t) pthread_join(t, NULL)
#endif
