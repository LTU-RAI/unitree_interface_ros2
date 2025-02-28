ROS2 package which exposes cmd_vel Twist topics for the Unitree Go1 robots.

Clone into workspace and colcon build (tip: use ```colcon build --symlink-install``` to be able to modify network setup without rebuilding).

The multiagent_interface node is for controlling one or more Go1s from a remote computer over wifi.
1. Connect the remote computer to the Concept Lab router. Select a static IP if possible, otherwise take note of the IP address.
2. Edit multiagent_interface.py, line 10 ```local_ip_wifi = '192.168.50.xxx'```, replace with your IP address.
3. Start the interface with (for example) ```ros2 run unitree_interface multiagent_interface 1 2``` to controll unitree1 and unitree2.
4. Publish velocity commands to unitreeX/cmd_vel (where X is 1, 2 or 3)
