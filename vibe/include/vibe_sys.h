#ifndef VIBE_SYS_H
#define VIBE_SYS_H
#if defined(_WIN32)
    #define VIBE_OS_WINDOWS
#elif defined(__linux__)
    #define VIBE_OS_LINUX
#elif defined(__APPLE__)
    #define VIBE_OS_MACOS
#endif
#endif
