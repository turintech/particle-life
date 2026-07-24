cmake_minimum_required(VERSION 3.16)
project(swarm_garden LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(swarm_sim src/simulation.cpp)
target_include_directories(swarm_sim PUBLIC src)
target_compile_options(swarm_sim PRIVATE -Wall -Wextra -Wpedantic)

add_executable(swarm_garden src/main.cpp)
target_link_libraries(swarm_garden PRIVATE swarm_sim)
target_compile_options(swarm_garden PRIVATE -Wall -Wextra -Wpedantic)

enable_testing()
add_executable(swarm_tests tests/simulation_test.cpp)
target_link_libraries(swarm_tests PRIVATE swarm_sim)
target_compile_options(swarm_tests PRIVATE -Wall -Wextra -Wpedantic)
add_test(NAME simulation COMMAND swarm_tests)
