#!/usr/bin/env python3
"""
Điều khiển OpenManipulator-X tự động lặp: HOME → INIT → HOME → INIT...
Có điều khiển gripper open/close
"""
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState
from control_msgs.action import GripperCommand
from builtin_interfaces.msg import Duration
import sys


class OpenManipulatorAutoLoop(Node):
    def __init__(self):
        super().__init__('om_auto_loop')
        
        # Parameters
        self.declare_parameter('duration', 2.0)  # Thời gian di chuyển mỗi lần
        self.declare_parameter('pause', 1.0)     # Thời gian dừng giữa các lần
        self.declare_parameter('loops', -1)      # Số vòng lặp (-1 = vô hạn)
        self.declare_parameter('gripper', True)  # Bật/tắt gripper
        
        self.duration = self.get_parameter('duration').value
        self.pause_time = self.get_parameter('pause').value
        self.max_loops = self.get_parameter('loops').value
        self.use_gripper = self.get_parameter('gripper').value
        
        # Define poses
        self.poses = {
            'HOME': [0.0, -1.0, 0.7, 0.3],
            'VAT': [0.0, -1.0, 1.0, 0.3],
            'INIT': [0.0, 0.0, 0.0, 0.0]
        }
        
        self.pose_sequence = ['HOME','INIT']  # Trình tự: HOME -> INIT -> HOME -> ...
        self.current_pose_idx = 0
        self.loop_count = 0
        
        # Joint names
        self.joint_names = ['joint1', 'joint2', 'joint3', 'joint4']
        
        # Publisher
        self.trajectory_pub = self.create_publisher(
            JointTrajectory,
            '/arm_controller/joint_trajectory',
            10
        )
        
        # Subscriber
        self.joint_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_callback,
            10
        )
        
        self.current_joints = None
        self.is_moving = False
        self.target_joints = None
        
        # Gripper action client
        if self.use_gripper:
            self.gripper_client = ActionClient(
                self,
                GripperCommand,
                '/gripper_controller/gripper_cmd'
            )
        
        # Log
        self.get_logger().info('OpenManipulator Auto Loop Started')
        if self.use_gripper:
            self.get_logger().info('Gripper control: ENABLED')
        if self.max_loops > 0:
            self.get_logger().info(f'Loops: {self.max_loops}')
        else:
            self.get_logger().info('Loops: INFINITE')
        
        # Đợi joint states
        self.init_timer = self.create_timer(0.1, self.check_ready)
    
    def joint_callback(self, msg):
        """Callback nhận trạng thái khớp"""
        joints = {}
        for i, name in enumerate(msg.name):
            joints[name] = msg.position[i]
        
        try:
            self.current_joints = [
                joints['joint1'],
                joints['joint2'],
                joints['joint3'],
                joints['joint4']
            ]
        except KeyError:
            pass
    
    def check_ready(self):
        """Kiểm tra đã nhận được joint states chưa"""
        if self.current_joints is not None:
            self.init_timer.cancel()
            self.start_timer = self.create_timer(0.5, self.start_first_move)
            self.start_timer_fired = False
    
    def start_first_move(self):
        """Bắt đầu di chuyển lần đầu"""
        if not hasattr(self, 'start_timer_fired') or self.start_timer_fired:
            return
        self.start_timer_fired = True
        self.start_timer.cancel()
        
        self.send_next_trajectory()
        self.check_timer = self.create_timer(0.1, self.check_arrived)
    
    def send_next_trajectory(self):
        """Gửi trajectory tới pose tiếp theo"""
        pose_name = self.pose_sequence[self.current_pose_idx]
        self.target_joints = self.poses[pose_name]
        
        self.get_logger().info(f'Loop {self.loop_count + 1} -> {pose_name}')
        
        # Điều khiển gripper: HOME = close, INIT = open
        if self.use_gripper:
            if pose_name == 'HOME':
                self.control_gripper(0.0)  # close
            else:  # INIT
                self.control_gripper(0.01)  # open
        
        # Tạo trajectory message
        traj = JointTrajectory()
        traj.joint_names = self.joint_names
        
        point = JointTrajectoryPoint()
        point.positions = self.target_joints
        point.velocities = [0.0] * 4
        point.accelerations = [0.0] * 4
        point.time_from_start = Duration(
            sec=int(self.duration), 
            nanosec=int((self.duration % 1) * 1e9)
        )
        
        traj.points = [point]
        
        self.trajectory_pub.publish(traj)
        self.is_moving = True
    
    def control_gripper(self, position, effort=1.0):
        """Điều khiển gripper"""
        goal = GripperCommand.Goal()
        goal.command.position = float(position)
        goal.command.max_effort = float(effort)
        self.gripper_client.send_goal_async(goal)
    
    def check_arrived(self):
        """Kiểm tra đã đến đích chưa"""
        if not self.is_moving or self.current_joints is None or self.target_joints is None:
            return
        
        # Tính error
        errors = [abs(self.target_joints[i] - self.current_joints[i]) for i in range(4)]
        max_error = max(errors)
        
        if max_error < 0.02:  # threshold 0.02 rad
            pose_name = self.pose_sequence[self.current_pose_idx]
            self.is_moving = False
            
            # Chuyển sang pose tiếp theo
            self.current_pose_idx = (self.current_pose_idx + 1) % len(self.pose_sequence)
            
            # Tăng loop count khi hoàn thành 1 chu kỳ
            if self.current_pose_idx == 0:
                self.loop_count += 1
                
                # Kiểm tra đã đủ số vòng chưa
                if self.max_loops > 0 and self.loop_count >= self.max_loops:
                    self.get_logger().info(f'Completed {self.loop_count} loops')
                    self.check_timer.cancel()
                    self.shutdown_timer = self.create_timer(1.0, self.shutdown_node)
                    self.shutdown_fired = False
                    return
            
            # Đợi pause_time rồi di chuyển tiếp
            self.next_move_timer = self.create_timer(self.pause_time, self.continue_next_move)
            self.next_move_fired = False
    
    def continue_next_move(self):
        """Tiếp tục di chuyển sau khi dừng"""
        if self.next_move_fired:
            return
        self.next_move_fired = True
        self.next_move_timer.cancel()
        self.send_next_trajectory()
    
    def shutdown_node(self):
        """Thoát node"""
        if hasattr(self, 'shutdown_fired') and self.shutdown_fired:
            return
        if hasattr(self, 'shutdown_fired'):
            self.shutdown_fired = True
            self.shutdown_timer.cancel()
        self.get_logger().info('Shutting down...')
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    
    node = OpenManipulatorAutoLoop()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Stopped by user')
    finally:
        node.destroy_node()


if __name__ == '__main__':
    main()