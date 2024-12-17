FROM ubuntu:22.04

# Install packages
RUN apt-get update && apt-get install -y \
    curl \
    gcc git g++ \
    iproute2 \
    locales \
    make \
    python3-pip \
    tini \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Locales
RUN locale-gen en_US en_US.UTF-8
RUN update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
ENV LANG=en_US.UTF-8

# Universe
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
    -o /usr/share/keyrings/ros-archive-keyring.gpg

# Install ROS2
RUN echo "deb [arch=$(dpkg --print-architecture) \
    signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \ 
    http://packages.ros.org/ros2/ubuntu $(. /etc/os-release \
    && echo $UBUNTU_CODENAME) main" \
    | tee /etc/apt/sources.list.d/ros2.list >/dev/null

RUN apt update && DEBIAN_FRONTEND=noninteractive apt install -y \
    ros-dev-tools \
    ros-humble-ros-base \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    autopep8==2.3.1 \
    flake8==7.1.1 \
    pycodestyle==2.12.1

RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["tail", "-f", "/dev/null"]
