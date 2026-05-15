# Install dependencies

sudo apt-get install -y \
  tmux \
  joystick

# Install udev rules

# Lidar

# Pad
sudo tee /etc/udev/rules.d/50-terios-gamepad.rules > /dev/null << 'EOF'
# Terios T3 controller
KERNEL=="js[0-9]*", SUBSYSTEM=="input", SYMLINK+="input/js_robot", ATTRS{name}=="SHANWAN PS3/PC Gamepad"
EOF

# Lidar
sudo tee /etc/udev/rules.d/51-ydlidar-laser.rules > /dev/null << 'EOF'
# Udev rule for the cp210x usb to serial converter used by rpilidar and ylidar lasers
SUBSYSTEM=="tty" ATTRS{idVendor}=="10c4" ATTRS{idProduct}=="ea60", MODE:="0777" SYMLINK+="ttyUSB_LASER"
EOF

# Nano Atom driver
sudo tee /etc/udev/rules.d/52-nano-atom-driver.rules > /dev/null << 'EOF'
# Raspberry Pi UART for Nano Atom based driver
KERNEL=="ttyS0", SYMLINK+="ttyS_NANO_ATOM", MODE="0666"
EOF

# Restart udev rules. 
# TODO(robert): More tests on RPi
sudo udevadm control --reload-rules && sudo udevadm trigger && sudo systemctl restart udev
# sudo service udev reload && sudo service udev restart && sudo udevadm trigger