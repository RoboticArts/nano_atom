cmake_minimum_required(VERSION 3.8)
project(nano_atom_gz_sim)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

install(DIRECTORY
  config
  launch
  worlds
  models
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)

endif()

# Register hooks
ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/env-hooks/nano_atom_gz_sim.sh.in")

ament_package()
