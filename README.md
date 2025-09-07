![Status](https://img.shields.io/badge/status-active-success) [![CI](https://github.com/RoboticArts/nano_atom/actions/workflows/ci.yaml/badge.svg)](https://github.com/RoboticArts/nano_atom/actions/workflows/ci.yaml) ![Release](https://img.shields.io/github/v/release/roboticarts/nano_atom)


# Meet Nano Atom!
<p align="center">
<img src="docs/img/nano-atom-logo.png" alt="alt text" width="800"/>
</p>

Nano Atom is an open source mobile robot designed to emulate industrial ROS robots for universities preparing students for future robotics careers. 

<!-- [REAL NANO ATOM: WELDING STATION + NANO ATOM] -->

## 1. Quick start
*Requirements: Linux, Docker and X11*

<p align="center">
<img src="docs/img/nano-atom-sim.png" alt="alt text" width="800"/>
</p>

Get the docker compose file:

```
wget https://raw.githubusercontent.com/RoboticArts/nano_atom/refs/heads/jazzy-devel/docker/docker-compose.yaml
```

Enable GUI access for Docker:

```
xhost +local:root
```

Run Nano Atom:

```
docker compose up
```

Install CycloneDDS:

```
sudo apt-get update && sudo apt-get install ros-jazzy-rmw-cyclonedds-cpp
```

Set CycloneDDS:

```
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
```

Run teleop node:

```
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap cmd_vel:=/robot/robot_base_controller/cmd_vel -p stamped:=true
```

## 2. Installation

### 2.1. Setup

Create the workspace:

```
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws/src
```

Clone the repository:

```
git clone --branch jazzy-devel https://github.com/RoboticArts/nano_atom.git
```

### Option 1. Build from ROS2

Install dependencies:

```
cd ~/ros2_ws
rosdep update && rosdep install --from-paths src --ignore-src -y -r --rosdistro jazzy
```

Build the repository:

```
colcon build --symlink-install
source install/setup.bash
```

### Option 2. Build from Docker

Build the docker image:

```
cd ~/ros2_ws/src/nano_atom
docker compose -f docker/docker-compose.build.yaml build
```

<!-- docker build -t nano-atom:build -f docker/Dockerfile . --> 

## 3. Bringup

### 3.1. Setup

Go to the repository root directory:

```
cd ~/ros2_ws/src/nano_atom
```


### Option 1. ROS2 launch

Run `nano_atom` packages:

```
ros2 launch nano_atom_base base.launch.py
```

### Option 2. Docker container

Run `nano atom` containers:

```
docker compose -f docker/docker-compose.build.yaml up
```

## 5. Development

### 5.1 Docker container

The `docker-compose.dev.yaml` uses `docker-compose.yaml` to load the host repository as a volume
and source the workspace. 

Go to the repository root directory:

```
cd ~/ros2_ws/src/nano_atom
```


Build docker (if needed):

```
docker compose -f docker/docker-compose.dev.yaml build
```

Start docker containers:

```
docker compose -f docker/docker-compose.dev.yaml up
```

Go inside a container:

```
docker exec -it docker-nano-atom-1 bash
```


## 6. Architecture

This section details the **planned** architecture of the `nano_atom` robot from the perspective of robotics development, acting as the backend for high-level applications.

<p align="center">
<img src="docs/img/architecture.png" alt="alt text" width="700"/>
</p>

The software is arranged in different `modules`, each designed to accomplish a specific set of tasks. For example, localization focuses on guaranteeing the robot’s pose within an environment, while navigation provides a trajectory path.

The `modules` are based on a decoupled architecture, where communication between modules is allowed, but only through restrictive policies and standard interfaces. Together, they form the operative software (p.e. real time, control, etc), but they do not make decisions.

The `Robot Control System (RCS)` is responsible for decision-making, orchestrating and controlling each module. Its purpose is to translate high-level commands into concrete tasks for the modules.

The `Robotics Abstraction Layer (RAL)` provides a specification and a library that abstracts the logic of the `RCS` into standard commands using sockets. This ensures that user applications remain unchanged even if the internal logic evolves. 

The `RAL Client` provides access to the `RAL` interface in a specific programming language. With this design, developers do not need access to the library’s source code to execute commands on the robot, as all interactions are handled through the RAL Client via sockets.
