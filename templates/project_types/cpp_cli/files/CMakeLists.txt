cmake_minimum_required(VERSION 3.16)

project({{project_name}} LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(CTest)

add_executable({{project_id}} src/main.cpp)
target_compile_features({{project_id}} PRIVATE cxx_std_17)

add_executable({{project_id}}_smoke tests/test_smoke.cpp)
target_compile_features({{project_id}}_smoke PRIVATE cxx_std_17)

add_test(NAME {{project_id}}_smoke COMMAND {{project_id}}_smoke)
