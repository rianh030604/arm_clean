#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from control_msgs.msg import JointJog
from control_msgs.action import GripperCommand


class AMRArmController(Node):
    def __init__(self):
        super().__init__('amr_arm_controller')

        # ===============================
        # ARM SERVO (MoveIt Servo)
        # ===============================
        self.arm_pub = self.create_publisher(
            JointJog,
            '/servo_node/delta_joint_cmds',
            10
        )

        # publish 20Hz
        self.timer = self.create_timer(0.05, self.loop)

        # ===============================
        # GRIPPER ACTION
        # ===============================
        self.gripper_client = ActionClient(
            self,
            GripperCommand,
            '/gripper_controller/gripper_cmd'
        )

        self.get_logger().info('Waiting for gripper action server...')
        self.gripper_client.wait_for_server()
        self.get_logger().info('Gripper action server connected')

        # ===============================
        # STATE
        # ===============================
        self.active_joint = None
        self.velocity = 0.0
        self.wave_dir = 1
        self.step = 0
        self.step_time = self.get_clock().now()

        self.get_logger().info('AMR ARM + GRIPPER CONTROLLER STARTED')

    # ==================================================
    # ARM CONTROL
    # ==================================================
    def move_joint(self, joint_name, velocity):
        self.active_joint = joint_name
        self.velocity = float(velocity)

    def stop_arm(self):
        self.active_joint = None
        self.velocity = 0.0

    # ==================================================
    # GRIPPER CONTROL
    # ==================================================
    def gripper_open(self):
        self.send_gripper_goal(0.01)   # chỉnh theo URDF

    def gripper_close(self):
        self.send_gripper_goal(0.0)

    def send_gripper_goal(self, position, effort=1.0):
        goal = GripperCommand.Goal()
        goal.command.position = float(position)
        goal.command.max_effort = float(effort)

        self.gripper_client.send_goal_async(goal)

    # ==================================================
    # SERVO LOOP
    # ==================================================
    def loop(self):
        self.demo_sequence()

        if self.active_joint is None:
            return

        msg = JointJog()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'   # QUAN TRỌNG

        msg.joint_names = [self.active_joint]
        msg.velocities = [float(self.velocity)]
        msg.duration = 0.1

        self.arm_pub.publish(msg)

    # ==================================================
    # DEMO SEQUENCE (MỖI BƯỚC 3 GIÂY)
    # ==================================================
    def demo_sequence(self):
        now = self.get_clock().now()

        # mỗi bước cách nhau 3 giây
        if (now - self.step_time).nanoseconds < 3_000_000_000:
            return

        self.step_time = now

        # # ===== CHUỖI KHỞI ĐỘNG =====
        # if self.step == 0:
        #     self.get_logger().info('STEP 0: joint1 +')
        #     self.move_joint('joint1', 2.0)
        #     self.step += 1
        #     return

        # if self.step == 1:
        #     self.get_logger().info('STEP 1: stop arm')
        #     self.stop_arm()
        #     self.step += 1
        #     return

        # if self.step == 2:
        #     self.get_logger().info('STEP 2: joint2 +')
        #     self.move_joint('joint2', 2.0)
        #     self.step += 1
        #     return

        # if self.step == 3:
        #     self.get_logger().info('STEP 3: stop arm')
        #     self.stop_arm()
        #     self.step += 1
        #     return

        # ===== VÙNG VẪY TAY (LOOP JOINT4) =====
        if self.step == 0:
            self.get_logger().info(f'WAVE joint4 dir={self.wave_dir}')
            self.move_joint('joint4', 3.0 * self.wave_dir)

            # đảo chiều cho lần sau
            self.wave_dir *= -1

            # GIỮ step = 4 để lặp vô hạn
            return




# ==================================================
# MAIN
# ==================================================
def main(args=None):
    rclpy.init(args=args)
    node = AMRArmController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
