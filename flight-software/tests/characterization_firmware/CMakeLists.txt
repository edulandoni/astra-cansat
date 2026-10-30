cmake_minimum_required(VERSION 3.22)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS ON)

set(CHARACTERIZATION_TARGET "MPU" CACHE STRING "Sensor target: MPU or SOLAR")
set_property(CACHE CHARACTERIZATION_TARGET PROPERTY STRINGS MPU SOLAR)
string(TOUPPER "${CHARACTERIZATION_TARGET}" CHARACTERIZATION_TARGET)

if(NOT CHARACTERIZATION_TARGET STREQUAL "MPU" AND
   NOT CHARACTERIZATION_TARGET STREQUAL "SOLAR")
    message(FATAL_ERROR "CHARACTERIZATION_TARGET must be MPU or SOLAR")
endif()

project(characterization C ASM)

set(FLIGHT_COMPUTER_DIR "${CMAKE_CURRENT_SOURCE_DIR}/../../flight_computer")
add_executable(characterization)

# Reuse the hardware-validated CubeMX startup, peripheral setup, HAL, and linker
# script. The flight application itself is not linked into this target.
add_subdirectory("${FLIGHT_COMPUTER_DIR}/cmake/stm32cubemx"
                 "${CMAKE_CURRENT_BINARY_DIR}/stm32cubemx")

target_sources(characterization PRIVATE app_characterization.c)
target_include_directories(characterization PRIVATE "${FLIGHT_COMPUTER_DIR}/Core/Inc")
target_compile_options(characterization PRIVATE -Wall -Wextra -Wshadow -Wformat=2)

if(CHARACTERIZATION_TARGET STREQUAL "MPU")
    target_sources(characterization PRIVATE "${FLIGHT_COMPUTER_DIR}/Core/Src/mpu6500.c")
    target_compile_definitions(characterization PRIVATE CHARACTERIZE_MPU=1)
else()
    target_sources(characterization PRIVATE "${FLIGHT_COMPUTER_DIR}/Core/Src/ina3221.c")
    target_compile_definitions(characterization PRIVATE CHARACTERIZE_SOLAR=1)
endif()

# The shared toolchain file cannot choose this script because its source dir is
# this experimental project rather than flight_computer.
set(CMAKE_EXE_LINKER_FLAGS
    "-mcpu=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=hard -T \"${FLIGHT_COMPUTER_DIR}/STM32F411xx_FLASH.ld\" --specs=nano.specs -Wl,-Map=characterization.map -Wl,--gc-sections -Wl,--print-memory-usage")

target_link_libraries(characterization stm32cubemx)
