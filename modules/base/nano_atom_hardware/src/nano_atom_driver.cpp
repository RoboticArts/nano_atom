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

#include "nano_atom_hardware/nano_atom_driver.hpp"

NanoAtomDriver::NanoAtomDriver(const std::string& serial_port, const int serial_baudrate,
                                const int serial_timeout, const int resolution)
{
  std::cout << "Configure serial" << std::endl;
  (void)resolution;

  jit_ = std::make_unique<SerialJitbus>();
  
  if (jit_->init(serial_port.c_str(), serial_baudrate, serial_timeout))
  { 
    std::cout << "Serial port opened! \n";
  }

  hardware_thread_ = std::jthread(
    [this](std::stop_token st){
      hardware_loop(st);
  });

}

void NanoAtomDriver::hardware_loop(std::stop_token st)
{
  while(!st.stop_requested())
  {
    if (jit_->available() > 0)
    {
      std::lock_guard<std::mutex> lock(jitbus_mutex_); 
      jit_->receivePacket(motor_state_, 1);
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(1));
  }
}

void NanoAtomDriver::setWheelCommand(const DiffDriveCommand& command)
{
  motor_setpoint_[0] = static_cast<float>(command.left_wheel.velocity);
  motor_setpoint_[1] = static_cast<float>(command.right_wheel.velocity);

  jit_->sendPacket(motor_setpoint_, 2);
  
  //std::cout << "Set wheel commands! \n";
  //std::cout << "Left: " << motor_setpoint_[0] << "\n";
  //std::cout << "Right: " << motor_setpoint_[1] << "\n";
}

void NanoAtomDriver::getWheelState(DiffDriveState& state)
{
  std::lock_guard<std::mutex> lock(jitbus_mutex_);

  state.left_wheel.position = motor_state_.position[0];
  state.left_wheel.velocity = motor_state_.velocity[0];
  state.right_wheel.position = motor_state_.position[1];
  state.right_wheel.velocity = motor_state_.velocity[1];

  // std::cout << "Get wheel states! \n";
  // std::cout << "Left Wheel \n";
  // std::cout << " - Position: " << state.left_wheel.position << "\n";
  // std::cout << " - Velocity: " << state.left_wheel.velocity << "\n";
  // std::cout << "Right Wheel \n";
  // std::cout << " - Position: " << state.right_wheel.position << "\n";
  // std::cout << " - Velocity: " << state.right_wheel.velocity << "\n";
}

