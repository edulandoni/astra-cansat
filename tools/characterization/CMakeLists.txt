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
