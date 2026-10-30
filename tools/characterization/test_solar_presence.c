#include "solar_presence.h"

#include <stdio.h>

static int failures;

static void Expect(const char *name, bool actual, bool expected) {
    if (actual != expected) {
        (void)fprintf(stderr, "FAIL: %s (actual=%d expected=%d)\n", name, actual, expected);
        ++failures;
    }
}

int main(void) {
    const int32_t threshold_on_mV = 2000;
    const int32_t threshold_off_mV = 1000;

    Expect("OFF above ON becomes ON",
           SolarPresence_Update(2001, threshold_on_mV, threshold_off_mV, false),
           true);
    Expect("ON between thresholds remains ON",
           SolarPresence_Update(1500, threshold_on_mV, threshold_off_mV, true),
           true);
    Expect("ON below OFF becomes OFF",
           SolarPresence_Update(999, threshold_on_mV, threshold_off_mV, true),
           false);
    Expect("OFF between thresholds remains OFF",
           SolarPresence_Update(1500, threshold_on_mV, threshold_off_mV, false),
           false);

    return failures == 0 ? 0 : 1;
}
