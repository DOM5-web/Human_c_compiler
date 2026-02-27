/**
 * This header provides cryptographic primitives, including an optimized XOR cipher and DJB2 hashing.
 * In version 1.5.6, the XOR cipher remains specialized for 1, 4, and 8-byte keys using word-sized operations.
 * This code is AI-generated.
 */
#ifndef VIBE_CRYPT_H
#define VIBE_CRYPT_H

#include <stddef.h>
#include <stdint.h>
#include <string.h>

/**
 * vibe_xor_cipher - Simple XOR encryption/decryption
 * @data: Data to encrypt/decrypt (in-place)
 * @len: Length of data
 * @key: Key to use
 * @key_len: Length of key
 * Internal Logic: Uses word-sized XOR operations for common key sizes to maximize throughput.
 * Falls back to an optimized byte-wise loop for arbitrary key lengths.
 */
static inline void vibe_xor_cipher(uint8_t* data, size_t len, const uint8_t* key, size_t key_len) {
    if (!data || !key || key_len == 0) return;

    // BOLT: Specialization for 1-byte keys to use word-sized XOR operations.
    if (key_len == 1) {
        uint8_t k = key[0];
        uint64_t k8 = ((uint64_t)k << 56) | ((uint64_t)k << 48) | ((uint64_t)k << 40) | ((uint64_t)k << 32) |
                      ((uint64_t)k << 24) | ((uint64_t)k << 16) | ((uint64_t)k << 8) | (uint64_t)k;
        size_t i = 0;
        for (; i + 8 <= len; i += 8) {
            uint64_t d;
            memcpy(&d, &data[i], 8);
            d ^= k8;
            memcpy(&data[i], &d, 8);
        }
        for (; i < len; i++) {
            data[i] ^= k;
        }
        return;
    }

    // BOLT: Specialization for 4-byte keys to use word-sized XOR operations.
    if (key_len == 4) {
        uint32_t k4;
        memcpy(&k4, key, 4);
        uint64_t k8 = ((uint64_t)k4 << 32) | (uint64_t)k4;
        size_t i = 0;
        for (; i + 8 <= len; i += 8) {
            uint64_t d;
            memcpy(&d, &data[i], 8);
            d ^= k8;
            memcpy(&data[i], &d, 8);
        }
        for (; i < len; i++) {
            data[i] ^= key[i & 3];
        }
        return;
    }

    // BOLT: Specialization for 8-byte keys to allow word-sized XOR operations.
    if (key_len == 8) {
        uint64_t k8;
        memcpy(&k8, key, 8);
        size_t i = 0;
        for (; i + 8 <= len; i += 8) {
            uint64_t d;
            memcpy(&d, &data[i], 8);
            d ^= k8;
            memcpy(&data[i], &d, 8);
        }
        for (; i < len; i++) {
            data[i] ^= key[i & 7];
        }
        return;
    }

    // Internal Logic: Generic byte-wise XOR loop with incremental key index.
    size_t k = 0;
    for (size_t i = 0; i < len; i++) {
        data[i] ^= key[k++];
        if (k == key_len) k = 0;
    }
}

/**
 * vibe_simple_hash - A very simple non-cryptographic hash (DJB2)
 * Internal Logic: Classic DJB2 hash algorithm using bit shifts and additions.
 */
static inline uint64_t vibe_simple_hash(const char* str) {
    if (!str) return 0;
    uint64_t hash = 5381;
    int c;
    while ((c = *str++)) {
        hash = ((hash << 5) + hash) + c;
    }
    return hash;
}

#endif
