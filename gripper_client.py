#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from control_msgs.action import GripperCommand


class GripperClient(Node):
    def __init__(self):
        super().__init__('gripper_client')

        self.client = ActionClient(
            self,
            GripperCommand,
            '/gripper_controller/gripper_cmd'
        )

        self.get_logger().info('Waiting for gripper action server...')
        self.client.wait_for_server()
        self.get_logger().info('Gripper action server connected')

    def send_goal(self, position, effort=1.0):
        goal = GripperCommand.Goal()
        goal.command.position = float(position)
        goal.command.max_effort = float(effort)

        self.client.send_goal_async(
            goal,
            feedback_callback=self.feedback_cb
        ).add_done_callback(self.goal_response_cb)

    def goal_response_cb(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Gripper goal rejected')
            return

        self.get_logger().info('Gripper goal accepted')
        goal_handle.get_result_async().add_done_callback(self.result_cb)

    def result_cb(self, future):
        self.get_logger().info('Gripper action done')

    def feedback_cb(self, feedback):
        pass


def main():
    rclpy.init()
    node = GripperClient()

    # ===== TEST =====
    node.send_goal(0.01)   # open
    rclpy.spin_once(node, timeout_sec=2)

    node.send_goal(0.0)    # close
    rclpy.spin_once(node, timeout_sec=2)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
