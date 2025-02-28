#!/usr/bin/env python
import rclpy
from rclpy.node import Node
from unitree_interface.ucl.rosHandler import ROSHandler
from geometry_msgs.msg import Twist
from sys import argv

sendPort_high = 8082

local_ip_wifi = '192.168.50.242'

unitreeWifiAddr = {
  "unitree1": '192.168.50.201',
  "unitree2": '192.168.50.202',
  "unitree3": '192.168.50.203',
  "unitree4": '192.168.50.204'
}

listenPort = {
  "unitree1": 8091,
  "unitree2": 8092,
  "unitree3": 8093,
  "unitree4": 8094
}

class UnitreeInterface(Node):
    def __init__(self, name):
        super().__init__('unitree_ros2_interface', namespace=name)
        self.name = name
        self.handler = ROSHandler((listenPort[name], unitreeWifiAddr[name], sendPort_high, local_ip_wifi))
        self.create_subscription(Twist, "cmd_vel", self.velocityCommandCallback, 10)
        print(f"First Contact for {name}...")
        self.handler.firstContact()

    def velocityCommandCallback(self, data:Twist):
        lx = data.linear.x
        ly = data.linear.y
        yawRate = data.angular.z
        print(f"Sending velocity command to {self.name} --> lx: {lx}, ly: {ly}, Yaw rate: {yawRate}")

        self.handler.sendMovement(lx, ly, yawRate)

def main(args=None):
    rclpy.init(args=args)
    nodes = []
    for i in range(1, len(argv)):
        nodes.append(UnitreeInterface(f"unitree{argv[i]}"))

    while rclpy.ok():
      for node in nodes:
        try:
          rclpy.spin_once(node, timeout_sec=0.0001)

        except KeyboardInterrupt:
          rclpy.try_shutdown()

if __name__ == "__main__":
    main()