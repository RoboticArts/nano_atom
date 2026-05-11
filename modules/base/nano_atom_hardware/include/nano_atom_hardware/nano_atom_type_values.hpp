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

#include <string>

namespace nano_atom_type_values
{

		struct JointConfig {
      std::string name = "";
    };

		struct JointState {
    	double position = 0.0;
      double velocity = 0.0;
    };

		struct JointCommand {
    	double position = 0.0;
      double velocity = 0.0;
    };

    template <typename JointT>
    struct DiffDrive {
      JointT left_wheel;
      JointT right_wheel;
    };

		using DiffDriveConfig = DiffDrive<JointConfig>;
		using DiffDriveState = DiffDrive<JointState>;
    using DiffDriveCommand = DiffDrive<JointCommand>;

}