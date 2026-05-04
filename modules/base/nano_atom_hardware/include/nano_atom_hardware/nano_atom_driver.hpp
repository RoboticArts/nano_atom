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
#define JITBUS_DISABLE_LOG

#include <iostream>
#include <thread>
#include <chrono>
#include <jitbus.h>

#include "nano_atom_hardware/nano_atom_type_values.hpp"

using DiffDriveState = nano_atom_type_values::DiffDriveState;
using DiffDriveCommand = nano_atom_type_values::DiffDriveCommand;

// TODO(robert): Implement this class as a library in nano_atom_lib repository
class NanoAtomDriver {

  public:

    NanoAtomDriver(const std::string& serial_port, const int serial_baudrate,
                    const int serial_timeout, const int resolution);
    virtual ~NanoAtomDriver() = default;

    void setWheelCommand(const DiffDriveCommand& command);
    void getWheelState(DiffDriveState& state);

  private:
    
    std::unique_ptr<SerialJitbus> jit_;
    std::jthread hardware_thread_;

    void hardware_loop(std::stop_token st);

    // Check
    struct MotorState
    { 
      float position[4];
      float velocity[4];
    };

    float motor_setpoint_[4]{0.0};

    MotorState motor_state_;

    std::mutex jitbus_mutex_;

};