# test world

This package includes test world and robot spawn scripts.

The package has QR-coded table models that placed on a test area from turtlebot3_gazebo package.

To create a wold with QR-coded tables:
```
$ ros2 launch test_world create_world.py
```
To spawn a robot:
```
$ ros2 launch test_world spawn_robot.py
```
You need turtlebot3_gazebo package installed.

