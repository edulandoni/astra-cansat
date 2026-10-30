#include "solar_presence.h"

bool SolarPresence_Update(int32_t voltage_mV,
                          int32_t threshold_on_mV,
                          int32_t threshold_off_mV,
                          bool previous_state) {
    if (previous_state) {
        return voltage_mV < threshold_off_mV ? false : true;
    }

    return voltage_mV > threshold_on_mV ? true : false;
}
