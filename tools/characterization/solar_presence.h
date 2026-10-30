#ifndef SOLAR_PRESENCE_H
#define SOLAR_PRESENCE_H

#include <stdbool.h>
#include <stdint.h>

bool SolarPresence_Update(int32_t voltage_mV,
                          int32_t threshold_on_mV,
                          int32_t threshold_off_mV,
                          bool previous_state);

#endif /* SOLAR_PRESENCE_H */
