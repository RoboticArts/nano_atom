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

NanoAtomDriver::NanoAtomDriver(const std::string& serial_port, const std::string& serial_baudrate,
                                const std::string& serial_timeout, const std::string& resolution)
{
  (void)serial_port;
  (void)serial_baudrate;
  (void)serial_timeout;
  (void)resolution;
  std::cout << "Configure serial" << std::endl;
}

bool NanoAtomDriver::setWheelCommand(const DiffDriveCommand& command)
{

  (void)command;
  std::cout << "Set wheel commands!" << std::endl;

  return true;
}

bool NanoAtomDriver::getWheelState(DiffDriveState& state)
{

  (void)state;
  std::cout << "Get wheel states!" << std::endl;

  return true;
}