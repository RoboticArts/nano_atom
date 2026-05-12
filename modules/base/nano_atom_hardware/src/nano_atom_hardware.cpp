// Copyright (C) 2025, Robotic Arts
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program. If not, see <https://www.gnu.org/licenses/>.
//
// Author: Robert Vasquez Zavaleta

#include "nano_atom_hardware/nano_atom_hardware.hpp"

namespace nano_atom_hardware
{

CallbackReturn NanoAtomSystem::on_init(const HardwareComponentInterfaceParams& params)
{

  if (SystemInterface::on_init(params) != CallbackReturn::SUCCESS) {
    return CallbackReturn::ERROR;
  }

  RCLCPP_INFO(logger_, "On init...");

  auto get_param = [&](const std::string& name)-> std::string {
      auto it = params.hardware_info.hardware_parameters.find(name);
      if (it == params.hardware_info.hardware_parameters.end()){
        RCLCPP_ERROR(logger_, "Missing required hardware parameter: %s", name.c_str());  
        throw std::runtime_error("Missing hardware paramter");
      };
      return it->second;
  };

  // Wheels
  config_.diff_drive.left_wheel.name = get_param("left_wheel_joint_name");
  config_.diff_drive.right_wheel.name = get_param("right_wheel_joint_name");

  // Serial port
  config_.serial_port = get_param("serial_port");
  config_.serial_baudrate =  std::stoi(get_param("serial_baudrate"));
  config_.serial_timeout =  std::stoi(get_param("serial_timeout"));

  // Others
  config_.resolution =  std::stoi(get_param("resolution"));

  RCLCPP_INFO(logger_, "Finished On init.");

  return hardware_interface::CallbackReturn::SUCCESS;
}

CallbackReturn NanoAtomSystem::on_configure(const rclcpp_lifecycle::State& /*previous_state*/)
{
  
  RCLCPP_INFO(logger_, "On configure...");

  RCLCPP_INFO(logger_, "Finished Configuration");

  return hardware_interface::CallbackReturn::SUCCESS;
}


std::vector<StateInterface> NanoAtomSystem::export_state_interfaces()
{

  std::vector<StateInterface> state_interfaces;

  // Left wheel, position
  state_interfaces.emplace_back(
        hardware_interface::StateInterface(config_.diff_drive.left_wheel.name,
          hardware_interface::HW_IF_POSITION, &diff_drive_state_.left_wheel.position)
      );

  // Left wheel, velocity
  state_interfaces.emplace_back(
          hardware_interface::StateInterface(config_.diff_drive.left_wheel.name,
            hardware_interface::HW_IF_VELOCITY, &diff_drive_state_.left_wheel.velocity)
        );

  // Right wheel, position
  state_interfaces.emplace_back(
        hardware_interface::StateInterface(config_.diff_drive.right_wheel.name,
          hardware_interface::HW_IF_POSITION, &diff_drive_state_.right_wheel.position)
      );

  // Right wheel, velocity
  state_interfaces.emplace_back(
          hardware_interface::StateInterface(config_.diff_drive.right_wheel.name,
            hardware_interface::HW_IF_VELOCITY, &diff_drive_state_.right_wheel.velocity)
        );

  return state_interfaces;
}

std::vector<CommandInterface> NanoAtomSystem::export_command_interfaces()
{

  std::vector<CommandInterface> command_interfaces;

  // Left wheel, position
  command_interfaces.emplace_back(
      hardware_interface::CommandInterface(config_.diff_drive.left_wheel.name,
        hardware_interface::HW_IF_POSITION, &diff_drive_command_.left_wheel.position
      ));

  // Left wheel, velocity
  command_interfaces.emplace_back(
      hardware_interface::CommandInterface(config_.diff_drive.left_wheel.name,
        hardware_interface::HW_IF_VELOCITY, &diff_drive_command_.left_wheel.velocity
      ));

  // Right wheel, position
  command_interfaces.emplace_back(
      hardware_interface::CommandInterface(config_.diff_drive.right_wheel.name,
        hardware_interface::HW_IF_POSITION, &diff_drive_command_.right_wheel.position
      ));

  // Right wheel, velocity
  command_interfaces.emplace_back(
      hardware_interface::CommandInterface(config_.diff_drive.right_wheel.name,
        hardware_interface::HW_IF_VELOCITY, &diff_drive_command_.right_wheel.velocity
      ));


  return command_interfaces;
}


CallbackReturn NanoAtomSystem::on_activate(const rclcpp_lifecycle::State& /* previous_state */)
{
  
  RCLCPP_INFO(logger_, "On activate...");
  
  // TODO(robert): Create nano_atom_sdk under the nano_atom_lib repository.
  //    Review the naming and add it as a submodule if needed.
  //    Dependency chain: libserial -> jitbus -> nano_atom_lib -> hw_interface/script,
  //    allowing only one active hardware owner at a time.
  //    Expose shared devices such as IMU, LEDs and buzzer through the SDK.
  nano_atom_driver_ = std::make_unique<NanoAtomDriver>( config_.serial_port, config_.serial_baudrate,
                                                        config_.serial_timeout, config_.resolution);

  RCLCPP_INFO(logger_, "Finished Activation");

  return CallbackReturn::SUCCESS;
}

CallbackReturn NanoAtomSystem::on_deactivate(const rclcpp_lifecycle::State& /* previous_state */)
{
  
  RCLCPP_INFO(logger_, "On deactivate...");
  RCLCPP_INFO(logger_, "Finished Deactivation");

  return CallbackReturn::SUCCESS;
}

ReturnType NanoAtomSystem::read(const rclcpp::Time& /* time */, const rclcpp::Duration& /* period */)
{
  
  //RCLCPP_INFO(logger_, "Read hardware interface!");
  nano_atom_driver_->getWheelState(diff_drive_state_);

  return hardware_interface::return_type::OK;
}

ReturnType NanoAtomSystem::write(const rclcpp::Time& /* time */, const rclcpp::Duration& /* period */)
{

  //RCLCPP_INFO(logger_, "Write hardware interface!");
  nano_atom_driver_->setWheelCommand(diff_drive_command_);

  return hardware_interface::return_type::OK;
}


}

PLUGINLIB_EXPORT_CLASS(nano_atom_hardware::NanoAtomSystem, SystemInterface)