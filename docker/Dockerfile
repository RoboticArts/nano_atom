
FROM osrf/ros:jazzy-desktop

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    ROBOT_USER=robot \
    ROBOT_DISTRO=jazzy \
    ROBOT_WS=/home/robot/ros2_ws

# Install utilities
RUN apt-get update && apt-get install -y \
    python3-colcon-common-extensions \
    python3-rosdep \
    git curl build-essential \
    bash-completion \
    && rm -rf /var/lib/apt/lists/*

# Install CycloneDDS
RUN apt-get update && apt-get install -y \
    ros-${ROBOT_DISTRO}-rmw-cyclonedds-cpp && \
    rm -rf /var/lib/apt/lists/*    

# Install Gazebo
RUN apt-get update && apt-get install -y curl lsb-release gnupg
RUN curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" \
    | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null && \
    sudo apt-get update && \
    sudo apt-get install gz-harmonic -y && \
    rm -rf /var/lib/apt/lists/*

# Add entrypoint
COPY docker/ros_entrypoint.sh /ros_entrypoint.sh
RUN chmod +x /ros_entrypoint.sh

# Create non root user
RUN useradd -ms /bin/bash ${ROBOT_USER} \
    && echo "${ROBOT_USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
USER ${ROBOT_USER}

# Workspace setup
RUN mkdir -p ${ROBOT_WS}/src
WORKDIR ${ROBOT_WS}

# Get repository
# RUN cd ${ROBOT_WS}/src && \
#     git clone --branch ${ROBOT_DISTRO}-devel https://github.com/RoboticArts/nano_atom.git
COPY . ${ROBOT_WS}/src/nano_atom

# Install dependencies
RUN cd ${ROBOT_WS} && \
    sudo apt-get update && \
    rosdep update && \
    rosdep install --from-paths src --ignore-src -y -r --rosdistro ${ROBOT_DISTRO} && \
    sudo rm -rf /var/lib/apt/lists/*

# Add bash
SHELL ["/bin/bash", "-c"]

# Build repository
RUN source /opt/ros/${ROBOT_DISTRO}/setup.bash && \
    cd ${ROBOT_WS} && \
    colcon build --symlink-install

# Source ros2 and ws for bash terminals
RUN echo "source /opt/ros/${ROBOT_DISTRO}/setup.bash" >> /home/${ROBOT_USER}/.bashrc && \
    echo "source ${ROBOT_WS}/install/setup.bash" >> /home/${ROBOT_USER}/.bashrc

ENTRYPOINT ["/ros_entrypoint.sh"]

CMD ["bash"]


