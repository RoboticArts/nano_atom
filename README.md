# nano_atom

Select a ROS workspace

```
cd ~/catkin_ws/src
```

Clone this repository

```
git clone https://github.com/RoboticArts/nano_atom.git
```

Clone Robotic Arts dependencies
```
git clone https://github.com/RoboticArts/roboticarts_sensors
```

Install ROS dependencies:

```
rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

Build and source the workspace:
```
cd ~/catkin_ws
catkin build
source devel/setup.bash
```


Launch nano atom sim:

```
roslaunch nano_atom_sim_bringup  nano_atom_complete.launch launch_localization:=true launch_navigation:=true
```