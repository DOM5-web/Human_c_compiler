#include <vibe_std.h>
#include <vibe_crypt.h>
#include <vibe_string.h>
#include <vibe_test.h>
#include <vibe_json.h>

void test_null_checks() {
    // These should not crash
    vibe_str_eq(NULL, "test");
    vibe_str_eq("test", NULL);
    vibe_str_eq(NULL, NULL);
    vibe_json_new_string(NULL);
    vibe_json_print(NULL);
    VIBE_ASSERT(true); // If we reached here, no crash
}

void test_constant_time_eq() {
    VIBE_ASSERT(vibe_str_eq_constant_time("test", "test") == true);
    VIBE_ASSERT(vibe_str_eq_constant_time("test", "fail") == false);
    VIBE_ASSERT(vibe_str_eq_constant_time("test", "test1") == false);
    VIBE_ASSERT(vibe_str_eq_constant_time("test1", "test") == false);
    VIBE_ASSERT(vibe_str_eq_constant_time(NULL, NULL) == true);
    VIBE_ASSERT(vibe_str_eq_constant_time(NULL, "test") == false);
}

int main() {
    test_null_checks();
    test_constant_time_eq();
    VIBE_TEST_SUMMARY();
    return 0;
}
