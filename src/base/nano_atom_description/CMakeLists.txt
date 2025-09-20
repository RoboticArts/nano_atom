cmake_minimum_required(VERSION 3.8)
project(nano_atom_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()


find_package(ament_cmake REQUIRED)

install(
  DIRECTORY
    launch
    config
    robots
    meshes
    urdf
  DESTINATION
    share/${PROJECT_NAME}/
)

if(BUILD_TESTING)

endif()

ament_package()
