cmake_minimum_required(VERSION 3.8)
project(nano_atom_hardware)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(hardware_interface REQUIRED)
find_package(pluginlib REQUIRED)
find_package(jitbus REQUIRED)

add_library(${PROJECT_NAME}
  SHARED
  src/nano_atom_hardware.cpp
  src/nano_atom_driver.cpp
)

target_include_directories(${PROJECT_NAME}
  PUBLIC
    $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

ament_target_dependencies(${PROJECT_NAME}
    rclcpp
    rclcpp_lifecycle
    hardware_interface
    pluginlib
)

target_link_libraries(${PROJECT_NAME}
  jitbus::jitbus
)

pluginlib_export_plugin_description_file(
  hardware_interface nano_atom_hardware.xml)

install(
  TARGETS ${PROJECT_NAME}
  EXPORT export_${PROJECT_NAME}
  LIBRARY DESTINATION lib
)

install(
  DIRECTORY include/
  DESTINATION include
)

install(
  FILES nano_atom_hardware.xml
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY
  config
  DESTINATION share/${PROJECT_NAME}
)

ament_export_targets(export_${PROJECT_NAME})
ament_export_dependencies(rclcpp rclcpp_lifecycle hardware_interface pluginlib)

if(BUILD_TESTING)

endif()

ament_package()
