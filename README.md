# ROS2 SDK

## Usage

```sh
chmod +x ./setup.py
./setup.py
```

## Useful Commands

```sh
ros2 pkg create --build-type ament_python <pkg_name>
ros2 pkg create --build-type ament_cmake <pkg_name>
```

```sh
colcon test --base-paths src/ --event-handlers console_cohesion+
colcon test --base-paths src/ --event-handlers console_cohesion+ --packages-select <pkg_name>
```

```sh
colcon build --base-paths src/
colcon build --base-paths src/ --packages-select <pkg_name>
colcon build --base-paths src/ -DCMAKE_BUILD_TYPE=Release
```

```sh
source install/setup.bash
```

## Additional Resources

- https://docs.ros.org/en/humble/index.html
