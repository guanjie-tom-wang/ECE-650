cmake_minimum_required(VERSION 2.8.12)
project(ece650-a4)

set(CMAKE_BUILD_TYPE Debug)

# Policy to handle the CMP0028 warning
if(POLICY CMP0028)
  cmake_policy(SET CMP0028 NEW)
endif()

if (EXISTS "${CMAKE_SOURCE_DIR}/minisat")
  add_subdirectory(minisat)
else()
  message (FATAL_ERROR "MiniSat not found. Use `git clone https://git.uwaterloo.ca/ece650-f23/minisat.git` to check it out.")
endif()

# enable c++11 support
set (CMAKE_CXX_FLAGS "-std=c++11 -Wall ${CMAKE_CXX_FLAGS}")
# expose minisat header files
include_directories(${CMAKE_SOURCE_DIR}/minisat)

option(WITH_ASAN "Enabled AddressSanitizer to detect memory faults" OFF)
if(WITH_ASAN)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address,undefined" )
endif()

# create the main executable
## add additional .cpp files if needed
add_executable(ece650-prj ece650-prj.cpp vertex.cpp)

set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -g")
set_target_properties(ece650-prj PROPERTIES COMPILE_FLAGS "-g" LINK_FLAGS "-g")

# link MiniSAT libraries
target_link_libraries(ece650-prj minisat-lib-static)

# Find and link pthread
find_package(Threads REQUIRED)
if(THREADS_HAVE_PTHREAD_ARG)
  target_compile_options(ece650-prj PUBLIC "-pthread")
endif()
if(CMAKE_THREAD_LIBS_INIT)
  target_link_libraries(ece650-prj "${CMAKE_THREAD_LIBS_INIT}")
endif()

# create the executable for tests
add_executable(test test.cpp)
# link MiniSAT libraries
target_link_libraries(test minisat-lib-static)
