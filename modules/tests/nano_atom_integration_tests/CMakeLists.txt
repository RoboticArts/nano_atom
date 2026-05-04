cmake_minimum_required(VERSION 3.8)
project(nano_atom_integration_tests)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(launch_testing_ament_cmake REQUIRED)

install(DIRECTORY
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  add_launch_test(
    test/test_smoke_base.py
    TARGET test_base_starts
  )
endif()

ament_package()
