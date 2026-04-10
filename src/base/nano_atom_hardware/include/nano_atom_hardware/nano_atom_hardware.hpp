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

#pragma once

#include <pluginlib/class_list_macros.hpp>

#include <rclcpp/rclcpp.hpp>
#include <rclcpp_lifecycle/state.hpp>
#include <rclcpp_lifecycle/node_interfaces/lifecycle_node_interface.hpp>
#include <hardware_interface/hardware_info.hpp>
#include <hardware_interface/system_interface.hpp>
#include <hardware_interface/types/hardware_interface_return_values.hpp>

#include "nano_atom_hardware/nano_atom_type_values.hpp"
#include "nano_atom_hardware/nano_atom_driver.hpp"

using SystemInterface = hardware_interface::SystemInterface;
using CallbackReturn = hardware_interface::CallbackReturn;
using HardwareComponentInterfaceParams = hardware_interface::HardwareComponentInterfaceParams;
using StateInterface = hardware_interface::StateInterface;
using CommandInterface = hardware_interface::CommandInterface;
using ReturnType = hardware_interface::return_type;
using DiffDriveConfig =nano_atom_type_values::DiffDriveConfig;
using DiffDriveState =nano_atom_type_values::DiffDriveState;
using DiffDriveCommand =nano_atom_type_values::DiffDriveCommand;

namespace nano_atom_hardware{

class NanoAtomSystem : public hardware_interface::SystemInterface {

  public:

		NanoAtomSystem() = default;
		virtual ~NanoAtomSystem() = default;

		CallbackReturn on_init(
      const HardwareComponentInterfaceParams& params) override;
		CallbackReturn on_configure(
      const rclcpp_lifecycle::State& previous_state) override;

		std::vector<StateInterface> export_state_interfaces() override;
		std::vector<CommandInterface> export_command_interfaces() override;

		CallbackReturn on_activate(
      const rclcpp_lifecycle::State& previous_state) override;
		CallbackReturn on_deactivate(
      const rclcpp_lifecycle::State& previous_state) override;
		
    ReturnType read(
      const rclcpp::Time& time, const rclcpp::Duration& period) override;
		ReturnType write(
      const rclcpp::Time& time, const rclcpp::Duration& period) override;

  private:

		rclcpp::Logger logger_{rclcpp::get_logger("NanoAtomSystem")};
    
    struct Config {
      std::string serial_port;
      std::string serial_baudrate;
      std::string serial_timeout;
      std::string resolution;
      DiffDriveConfig diff_drive;
    };

    Config config_;
    DiffDriveState diff_drive_state_;
		DiffDriveCommand diff_drive_command_;

    std::shared_ptr<NanoAtomDriver> nano_atom_driver_;

};

}

