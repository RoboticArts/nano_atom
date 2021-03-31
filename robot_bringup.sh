#!/bin/bash

export ROBOT_WORKSPACE=~/catkin_ws  # Robot workspace path
export ROBOT_FOLDER=`dirname "$0"`  # Robot package path

echo "Nano Atom auto-start!"

source $ROBOT_WORKSPACE/devel/setup.bash 
source $ROBOT_FOLDER/robot_params.env

export ROSMON_COLOR_MODE=256colors
export DISPLAY=:0
export XAUTHORITY=/run/user/1000/gdm/Xauthority

run_screen() {
  
  name=$1
  command=$2

  screen -dmS $name bash; 
  screen -S $name -X stuff "source /opt/ros/$ROS_DISTRO/setup.bash\n";
  screen -S $name -X stuff "source $ROBOT_WORKSPACE/devel/setup.bash\n";
  screen -S $name -X stuff "source $ROBOT_FOLDER/robot_params.env\n";
  screen -S $name -X stuff "$command\n";
  sleep 1;
} 



echo "killall screens..."
killall screen
sleep 3;

echo "Starting roscore..."
run_screen "core" "roscore";


if [[ -z $ROBOT_AUTOBOOT ]]; then
   ROBOT_AUTOBOOT=false
fi

echo "RUN SIMULATION = $ROBOT_RUN_SIMULATION"
echo "RUN RVIZ = $ROBOT_RUN_RVIZ"
echo "RUN TELEOP = $ROBOT_RUN_TELEOP"
echo "RUN LOCALIZATION = $ROBOT_RUN_LOCALIZATION"
echo "RUN NAVIGATION = $ROBOT_RUN_NAVIGATION"


if $ROBOT_RUN_SIMULATION 
then
  echo "Launching bringup simulation..."
  if $ROBOT_AUTOBOOT
  then
     run_screen "bringup" "mon launch nano_atom_sim_bringup nano_atom_complete.launch launch_rviz:=false gazebo_gui:=false";
  else
     run_screen "bringup" "mon launch nano_atom_sim_bringup nano_atom_complete.launch";
  fi
else
  echo "Launching bringup robot"
  run_screen "bringup" "mon launch nano_atom_bringup nano_atom_complete.launch";
fi

sleep 2;

if $ROBOT_RUN_TELEOP 
then
  echo "Launching robot teleop..."

  if [[ $ROBOT_PAD_DRIVER == "ds4drv" ]]
  then
    	run_screen "ds4drv" "ds4drv --hidraw";  
  fi

  run_screen  "teleop" "mon launch nano_atom_teleop teleop_complete.launch";
  
fi


if $ROBOT_RUN_LOCALIZATION
then
  echo "Launching robot localization..."
  run_screen  "localization" "roslaunch nano_atom_localization localization_complete.launch";
fi

if $ROBOT_RUN_NAVIGATION 
then
  echo "Launching robot navigation.."
  run_screen  "navigation" "roslaunch nano_atom_navigation navigation_complete.launch";
fi



