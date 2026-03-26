#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped, Pose
from tf2_ros import Buffer, TransformListener
from rclpy.action import ActionClient
from control_msgs.action import GripperCommand

# THƯ VIỆN CỦA CODE CŨ (Dùng bộ não OMPL) 
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import Constraints, OrientationConstraint, PositionConstraint, RobotState, BoundingVolume
from shape_msgs.msg import SolidPrimitive

import json
import math

JOINT_NAMES = ['joint1', 'joint2', 'joint3', 'joint4']
ARRIVE_THRESHOLD = 0.02
PAUSE_BETWEEN = 1.0
DEAD_ZONE = 0.001  

# ── Điểm trung gian khi đi LÊN (z tăng) ──
TRUNGGIAN_POINT_UP = {
    "x": 0.44, "y": 0.0, "z": 0.35,
    "qx": 0.964, "qy": 0.0, "qz": 0.266, "qw": 0.000,
    "order": [[2, 3], [4], ["check_dir"]],
}

# ── Điểm trung gian khi đi XUỐNG (z giảm) ──
TRUNGGIAN_POINT_DOWN = {
    "x": 0.44, "y": 0.0, "z": 0.35,
    "qx": 0.007, "qy": 0.004, "qz": 0.000, "qw": 1.000,
    "order": [[2, 3], [4], ["check_dir"]],
}

file_path = 'my_trajectory.json' 

try:
    with open(file_path, 'r') as f:
        POINTS = json.load(f)
except FileNotFoundError:
    print(f"❌ Không tìm thấy file {file_path}. Đang để POINTS trống.")
    POINTS = []

class ArmPubPoints(Node):
    def __init__(self):
        super().__init__('arm_pub_points')

        self.pub = self.create_publisher(String, '/arm_goal', 10)
        self.sub = self.create_subscription(JointState, '/joint_states', self.joint_callback, 10)
        
        # 🔥 ĐỔI SANG DÙNG MOVEGROUP ACTION CỦA CODE CŨ 🔥
        self.move_client = ActionClient(self, MoveGroup, 'move_action')
        self.get_logger().info("Đang chờ MoveGroup Server...")
        self.move_client.wait_for_server()
        self.get_logger().info("[INIT] MoveGroup Action READY")
        
        # Setup Gripper
        self.gripper_client = ActionClient(self, GripperCommand, '/gripper_controller/gripper_cmd')
        self.gripper_client.wait_for_server()
        self.get_logger().info("[INIT] Gripper action READY")
        
        # Setup TF
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Variables
        self.current_joints = None
        self.ik_result = None
        self.point_idx = 0
        self.step_idx = 0
        self.state = 'go_home'
        self.target_step = None
        self.pause_start = None
        self.flip_done = False
        self.prev_z = None

        self.create_timer(0.1, self.tick)

    # ───────────── ROS CALLBACKS ─────────────
    def joint_callback(self, msg):
        try:
            joints = dict(zip(msg.name, msg.position))
            self.current_joints = [joints[j] for j in JOINT_NAMES]
        except Exception:
            pass

    def get_current_tf(self):
        try:
            return self.tf_buffer.lookup_transform('world', 'end_effector_link', rclpy.time.Time())
        except Exception:
            return None

    # ───────────── GRIPPER CONTROL ─────────────
    def control_gripper(self, position, effort=1.0):
        goal = GripperCommand.Goal()
        goal.command.position = float(position)
        goal.command.max_effort = float(effort)

        self.get_logger().info(f"[GRIPPER] CMD → pos={position:.3f}")
        send_future = self.gripper_client.send_goal_async(goal, feedback_callback=lambda _: None)
        send_future.add_done_callback(self.gripper_goal_response_cb)

    def gripper_goal_response_cb(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.state = 'pause'
            return
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.gripper_result_cb)

    def gripper_result_cb(self, future):
        self.step_idx += 1
        self.state = 'pause'
        self.pause_start = self.get_clock().now()

    # ───────────── MONITOR & TRUNGGIAN & FLIP (GIỮ NGUYÊN) ─────────────
    def monitor_direction(self):
        t = self.get_current_tf()
        if not t: return
        z = t.transform.translation.z
        x, y = t.transform.translation.x, t.transform.translation.y
        if self.prev_z is not None:
            dz = z - self.prev_z
            if abs(dz) > DEAD_ZONE:
                direction = "↑ UP" if dz > 0 else "↓ DOWN"
                self.get_logger().info(f"[TF] {direction} | z={z:.4f}m dz={dz:+.4f} (x={x:.3f} y={y:.3f})")
        self.prev_z = z

    def select_trunggian(self, trunggian_idx):
        next_real_idx = trunggian_idx + 1
        while next_real_idx < len(POINTS) and POINTS[next_real_idx] is None: next_real_idx += 1
        if next_real_idx >= len(POINTS):
            POINTS[trunggian_idx] = TRUNGGIAN_POINT_UP
            return
        target_z = POINTS[next_real_idx]['z']
        t = self.get_current_tf()
        if not t:
            POINTS[trunggian_idx] = TRUNGGIAN_POINT_UP
            return
        current_z = t.transform.translation.z
        if (target_z - current_z) > 0: POINTS[trunggian_idx] = TRUNGGIAN_POINT_UP
        else: POINTS[trunggian_idx] = TRUNGGIAN_POINT_DOWN

    def check_q_target(self):
        if self.current_joints is None: return True
        next_real_idx = self.point_idx + 1
        while next_real_idx < len(POINTS) and POINTS[next_real_idx] is None: next_real_idx += 1
        if next_real_idx >= len(POINTS): return True

        target_pt = POINTS[next_real_idx]
        x, y = target_pt['x'], target_pt['y']

        desired_j1 = math.atan2(y, x)
        desired_j1 = math.atan2(math.sin(desired_j1), math.cos(desired_j1))
        current_j1 = self.current_joints[0]
        diff = abs(math.atan2(math.sin(desired_j1 - current_j1), math.cos(desired_j1 - current_j1)))

        if diff > 0.05 and not self.flip_done:
            self.flip_j1()
            self.flip_done = True
            return False  
        return True

    def flip_j1(self):
        if self.current_joints is None: return
        next_real_idx = self.point_idx + 1
        while next_real_idx < len(POINTS) and POINTS[next_real_idx] is None: next_real_idx += 1
        if next_real_idx >= len(POINTS): return

        target_pt = POINTS[next_real_idx]
        x, y = target_pt['x'], target_pt['y']
        desired_j1 = math.atan2(y, x)
        desired_j1 = math.atan2(math.sin(desired_j1), math.cos(desired_j1))

        if self.ik_result: self.ik_result[0] = desired_j1
        target = list(self.current_joints)
        target[0] = desired_j1
        
        goal = { "x": 0, "y": 0, "z": 0, "j1": target[0], "j2": target[1], "j3": target[2], "j4": target[3] }
        self.pub.publish(String(data=json.dumps(goal)))
        
        self.target_step = target
        self.state = 'wait_arrive'

    # BỘ NÃO OMPL TỪ CODE CŨ ĐƯỢC CẤY VÀO ĐÂY 
    def compute_ik(self):
        pt = POINTS[self.point_idx]
        if pt is None:
            self.point_idx += 1
            self.state = 'wait_ready'
            return

        self.get_logger().info("Đang nhờ MoveGroup (OMPL) suy nghĩ tìm dáng kẹp...")
        
        goal_msg = MoveGroup.Goal()
        goal_msg.request.group_name = "arm"
        goal_msg.request.allowed_planning_time = 10.0  # Cho 10 giây y như code cũ
        goal_msg.request.num_planning_attempts = 20

        constraints = Constraints()

        # 1. Ràng buộc Vị Trí (Hộp 1cm)
        pcm = PositionConstraint()
        pcm.header.frame_id = "world"
        pcm.link_name = "end_effector_link"
        cbox = BoundingVolume()
        cbox.primitives = [SolidPrimitive(type=SolidPrimitive.BOX, dimensions=[0.01, 0.01, 0.01])]
        
        target_pose = Pose()
        target_pose.position.x = float(pt['x'])
        target_pose.position.y = float(pt['y'])
        target_pose.position.z = float(pt['z'])
        cbox.primitive_poses = [target_pose]
        pcm.constraint_region = cbox
        pcm.weight = 1.0

        # 2. Ràng buộc Hướng (Sai số 0.1 rad y hệt code cũ)
        ocm = OrientationConstraint()
        ocm.header.frame_id = "world"
        ocm.link_name = "end_effector_link"
        ocm.orientation.x = float(pt['qx'])
        ocm.orientation.y = float(pt['qy'])
        ocm.orientation.z = float(pt['qz'])
        ocm.orientation.w = float(pt['qw'])
        ocm.absolute_x_axis_tolerance = 0.1
        ocm.absolute_y_axis_tolerance = 0.1
        ocm.absolute_z_axis_tolerance = 0.1
        ocm.weight = 1.0

        constraints.position_constraints.append(pcm)
        constraints.orientation_constraints.append(ocm)
        goal_msg.request.goal_constraints.append(constraints)

        # Lấy trạng thái hiện tại làm mốc
        if self.current_joints:
            js = JointState(name=JOINT_NAMES, position=self.current_joints)
            goal_msg.request.start_state = RobotState(joint_state=js)

        # ĐIỂM ĂN TIỀN: BẢO NÓ CHỈ TÍNH TOÁN, KHÔNG ĐƯỢC CHẠY MOTOR 
        goal_msg.planning_options.plan_only = True

        future = self.move_client.send_goal_async(goal_msg)
        future.add_done_callback(self.move_goal_cb)

    def move_goal_cb(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error("[OMPL] Goal rejected!")
            self.state = 'pause'
            return
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.move_result_cb)

    def move_result_cb(self, future):
        res = future.result().result
        if res.error_code.val != 1:
            self.get_logger().error(f"[OMPL] Không tìm ra dáng! (Mã lỗi: {res.error_code.val}) → skip")
            self.point_idx += 1
            self.state = 'wait_ready'
            return

        # Rút 4 góc khớp ở điểm cuối cùng của quỹ đạo mà OMPL vừa vẽ ra
        points = res.planned_trajectory.joint_trajectory.points
        if not points:
            self.get_logger().error("[OMPL] Quỹ đạo rỗng!")
            self.point_idx += 1
            self.state = 'wait_ready'
            return

        final_positions = points[-1].positions
        names = res.planned_trajectory.joint_trajectory.joint_names
        d = dict(zip(names, final_positions))
        
        # Nạp vào biến ik_result cho State Machine chạy
        self.ik_result = [d.get(j, 0.0) for j in JOINT_NAMES]

        self.get_logger().info(f"[OMPL] ĐÃ TÌM THẤY DÁNG KẸP SONG SONG: {self.ik_result}")
        self.state = 'run_step'

    # ───────────── EXECUTION ─────────────
    def run_step(self):
        pt = POINTS[self.point_idx]
        group = pt['order'][self.step_idx]

        if group == ["close"]:
            self.control_gripper(0.0, effort=3.0)
            self.state = 'wait_gripper'
            return
        elif group == ["open"]:
            self.control_gripper(0.01, effort=1.0)
            self.state = 'wait_gripper'
            return
        elif group == ["check_dir"]:
            if self.check_q_target():
                self.step_idx += 1
                self.state = 'pause'
                self.pause_start = self.get_clock().now()
            return

        if self.ik_result is None:
            return

        target = list(self.current_joints)
        for j in group:
            target[j - 1] = self.ik_result[j - 1]

        goal = { "x": pt['x'], "y": pt['y'], "z": pt['z'], "j1": target[0], "j2": target[1], "j3": target[2], "j4": target[3] }
        self.pub.publish(String(data=json.dumps(goal)))
        
        self.target_step = target
        self.state = 'wait_arrive'

    def arrived(self):
        if self.target_step is None: return False
        err = [abs(self.target_step[i] - self.current_joints[i]) for i in range(4)]
        return max(err) < ARRIVE_THRESHOLD

    # ───────────── MAIN STATE MACHINE ─────────────
    def tick(self):
        if self.current_joints is None: return
        self.monitor_direction()

        if self.state == 'go_home':
            goal = { "x": 0, "y": 0, "z": 0, "j1": 0, "j2": 0, "j3": 0, "j4": 0 }
            self.pub.publish(String(data=json.dumps(goal)))
            self.target_step = [0, 0, 0, 0]
            self.state = 'wait_home'

        elif self.state == 'wait_home':
            if self.arrived(): self.state = 'wait_ready'

        elif self.state == 'wait_ready':
            self.flip_done = False
            if POINTS[self.point_idx] is None:
                self.select_trunggian(self.point_idx)
            self.compute_ik()
            self.state = 'wait_ik'

        elif self.state in ['wait_gripper', 'wait_ik']: pass 
        elif self.state == 'run_step': self.run_step()
        elif self.state == 'wait_arrive':
            if self.arrived():
                self.step_idx += 1
                self.state = 'pause'
                self.pause_start = self.get_clock().now()

        elif self.state == 'pause':
            elapsed_time = (self.get_clock().now() - self.pause_start).nanoseconds / 1e9
            if elapsed_time > PAUSE_BETWEEN:
                order = POINTS[self.point_idx]['order']
                if self.step_idx >= len(order):
                    self.point_idx += 1
                    self.step_idx = 0
                    self.ik_result = None

                    # 🔥 NHỊP 1: XONG VIỆC -> DUỖI THẲNG TAY RA TRƯỚC (Giữ nguyên mâm j1) 🔥
                    if self.point_idx >= len(POINTS):
                        self.get_logger().info("🎉 [DONE] Đã chạy xong! Nhịp 1: Đang duỗi thẳng tay an toàn...")
                        
                        j1_curr = self.current_joints[0] if self.current_joints else 0.0
                        # Duỗi thẳng j2, j3, j4 về 0.0
                        stretch_joints = [j1_curr, 0.0, -1.5, 0.0] 
                        
                        goal = { "x": 0, "y": 0, "z": 0, "j1": stretch_joints[0], "j2": stretch_joints[1], "j3": stretch_joints[2], "j4": stretch_joints[3] }
                        self.pub.publish(String(data=json.dumps(goal)))
                        
                        self.target_step = stretch_joints
                        self.state = 'wait_stretch_end'
                        return
                    # ==========================================================
                    
                    self.state = 'wait_ready'
                else:
                    self.state = 'run_step'

        # 🔥 NHỊP 2: CHỜ DUỖI TAY XONG -> QUAY MÂM J1 VỀ 0 🔥
        elif self.state == 'wait_stretch_end':
            if self.arrived():
                self.get_logger().info("Nhịp 2: Đang xoay mâm (Flip J1) về trước...")
                
                # Giữ tay duỗi thẳng (0.0), chỉ xoay j1 về 0.0
                flip_joints = [0.0, 0.0, -1.5, 0.0] 
                
                goal = { "x": 0, "y": 0, "z": 0, "j1": flip_joints[0], "j2": flip_joints[1], "j3": flip_joints[2], "j4": flip_joints[3] }
                self.pub.publish(String(data=json.dumps(goal)))
                
                self.target_step = flip_joints
                self.state = 'wait_flip_end'

        # 🔥 NHỊP 3: CHỜ QUAY MÂM XONG -> GẬP VỀ TƯ THẾ NGHỈ (90°, -90°) 🔥
        elif self.state == 'wait_flip_end':
            if self.arrived():
                self.get_logger().info("Nhịp 3: Đang gập về TƯ THẾ NGHỈ...")
                
                # Mâm j1=0, gập vuông góc j2=90 độ (1.57rad) và j3=-90 độ (-1.57rad)
                relax_joints = [0.0, 1.5, -1.5, 0.0] 
                
                goal = { "x": 0, "y": 0, "z": 0, "j1": relax_joints[0], "j2": relax_joints[1], "j3": relax_joints[2], "j4": relax_joints[3] }
                self.pub.publish(String(data=json.dumps(goal)))
                
                self.target_step = relax_joints
                self.state = 'wait_relax'

        # 🔥 KẾT THÚC: CHỜ GẬP XONG -> TẮT MÁY 🔥
        elif self.state == 'wait_relax':
            if self.arrived():
                self.get_logger().info("💤 Robot đã đi ngủ an toàn. Tắt chương trình.")
                rclpy.shutdown()
def main():
    rclpy.init()
    node = ArmPubPoints()
    rclpy.spin(node)

if __name__ == '__main__':
    main()