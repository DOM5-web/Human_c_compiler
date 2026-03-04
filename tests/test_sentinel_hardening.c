/**
 * This test file verifies the newly implemented security hardening features, including vibe_str_copy and vibe_snprintf.
 * This code is AI-generated.
 */
#include "../vibe/include/vibe_string.h"
#include "../vibe/include/vibe_io.h"
#include "../vibe/include/vibe_test.h"
#include <string.h>

int main() {
    vibe_print("--- Vibe Sentinel Hardening Tests ---\n");

    // Test vibe_str_copy basic functionality
    char buf1[10];
    vibe_str_copy(buf1, "Hello", sizeof(buf1));
    VIBE_ASSERT_STR_EQ(buf1, "Hello");

    // Test vibe_str_copy truncation and null-termination
    char buf2[5];
    vibe_str_copy(buf2, "LongString", sizeof(buf2));
    VIBE_ASSERT_STR_EQ(buf2, "Long"); // Should be "Long" + \0
    VIBE_ASSERT_EQ(buf2[4], '\0');

    // Test vibe_str_copy with NULL src
    char buf3[10] = "Existing";
    vibe_str_copy(buf3, NULL, sizeof(buf3));
    VIBE_ASSERT_STR_EQ(buf3, "");

    // Test vibe_snprintf
    char buf4[20];
    vibe_snprintf(buf4, sizeof(buf4), "Value: %d", 42);
    VIBE_ASSERT_STR_EQ(buf4, "Value: 42");

    // Test vibe_snprintf truncation
    char buf5[5];
    vibe_snprintf(buf5, sizeof(buf5), "123456789");
    VIBE_ASSERT_STR_EQ(buf5, "1234");
    VIBE_ASSERT_EQ(buf5[4], '\0');

    VIBE_TEST_SUMMARY();
}
