#ifndef COMMAND_HANDLER_H
#define COMMAND_HANDLER_H

#include <stdint.h>

typedef enum {
    COMMAND_NONE,
    COMMAND_ZERO_ALTITUDE,
    COMMAND_SET_TIME,
    COMMAND_REQUEST_STATUS
} FlightCommand;

FlightCommand CommandHandler_DecodeDebugByte(uint8_t byte);
void CommandHandler_Execute(FlightCommand command);

#endif /* COMMAND_HANDLER_H */
