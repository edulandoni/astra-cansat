cmake_minimum_required(VERSION 3.16)
project(astra_characterization_host_tests C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

enable_testing()
add_executable(test_solar_presence test_solar_presence.c solar_presence.c)
target_compile_options(test_solar_presence PRIVATE
    $<$<C_COMPILER_ID:GNU,Clang>:-Wall;-Wextra;-Wpedantic>
    $<$<C_COMPILER_ID:MSVC>:/W4>)
add_test(NAME solar_presence COMMAND test_solar_presence)

add_executable(test_mpu6500_read_raw
    test_mpu6500_read_raw.c
    ../../flight-software/flight_computer/Core/Src/mpu6500.c)
target_include_directories(test_mpu6500_read_raw PRIVATE
    hal_mock
    ../../flight-software/flight_computer/Core/Inc)
target_compile_options(test_mpu6500_read_raw PRIVATE
    $<$<C_COMPILER_ID:GNU,Clang>:-Wall;-Wextra;-Wpedantic>
    $<$<C_COMPILER_ID:MSVC>:/W4>)
add_test(NAME mpu6500_read_raw COMMAND test_mpu6500_read_raw)
