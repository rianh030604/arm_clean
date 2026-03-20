#!/usr/bin/env python3
"""
Nhận goal từ file khác và điều khiển robot arm
Goal JSON: {"x": 0.2, "y": 0.0, "z": 0.1, "j1": 0.0, "j2": -0.5, "j3": 0.3, "j4": -0.1}
"""
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from std_msgs.msg import String
from builtin_interfaces.msg import Duration
import json


JOINT_NAMES = ['joint1', 'joint2', 'joint3', 'joint4']
MOVE_TIME = 2.0


class ArmServer(Node):
    def __init__(self):
        super().__init__('arm_server')

        self.pub = self.create_publisher(
            JointTrajectory,
            '/arm_controller/joint_trajectory',
            10
        )

        self.sub = self.create_subscription(
            String, '/arm_goal', self.goal_callback, 10)

        self.get_logger().info('Arm server ready! Listening on /arm_goal')
        self.get_logger().info('Format: {"x":0.2, "y":0.0, "z":0.1, "j1":0.0, "j2":-0.5, "j3":0.3, "j4":-0.1}')

    def goal_callback(self, msg):
        try:
            data = json.loads(msg.data)

            # Lấy joints - bắt buộc phải có
            j1 = data['j1']
            j2 = data['j2']
            j3 = data['j3']
            j4 = data['j4']

            # xyz - tuỳ chọn, chỉ để log biết đích đến
            x = data.get('x', None)
            y = data.get('y', None)
            z = data.get('z', None)

            if x is not None:
                self.get_logger().info(f'Target xyz: [{x:.3f}, {y:.3f}, {z:.3f}]')

            self.send([j1, j2, j3, j4])

        except KeyError as e:
            self.get_logger().error(f'Thiếu field: {e} | Cần đủ j1, j2, j3, j4')
        except json.JSONDecodeError:
            self.get_logger().error(f'JSON lỗi: {msg.data}')

    def send(self, positions):
        traj = JointTrajectory()
        traj.joint_names = JOINT_NAMES

        pt = JointTrajectoryPoint()
        pt.positions = [float(p) for p in positions]
        pt.velocities = [0.0] * 4
        pt.time_from_start = Duration(sec=int(MOVE_TIME))

        traj.points = [pt]
        self.pub.publish(traj)
        self.get_logger().info(f'Moving joints: {[f"{p:.3f}" for p in positions]}')


def main(args=None):
    rclpy.init(args=args)
    node = ArmServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()


if __name__ == '__main__':
    main()