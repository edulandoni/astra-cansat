#include "command_handler.h"

#include "sensor_manager.h"

FlightCommand CommandHandler_DecodeDebugByte(uint8_t byte) {
    if ((byte == (uint8_t)'Z') || (byte == (uint8_t)'z')) {
        return COMMAND_ZERO_ALTITUDE;
    }
    return COMMAND_NONE;
}

void CommandHandler_Execute(FlightCommand command) {
    switch (command) {
        case COMMAND_ZERO_ALTITUDE:
            SensorManager_StartAltitudeCalibration();
            break;
        case COMMAND_NONE:
        case COMMAND_SET_TIME:
        case COMMAND_REQUEST_STATUS:
        default:
            break;
    }
}
