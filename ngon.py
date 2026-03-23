#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from moveit_msgs.srv import GetPositionIK
from moveit_msgs.msg import PositionIKRequest, RobotState
from geometry_msgs.msg import PoseStamped
from tf2_ros import Buffer, TransformListener
from rclpy.action import ActionClient
from control_msgs.action import GripperCommand
import json
import math

JOINT_NAMES = ['joint1', 'joint2', 'joint3', 'joint4']
ARRIVE_THRESHOLD = 0.02
PAUSE_BETWEEN = 1.0
DEAD_ZONE = 0.001  

# ── Điểm trung gian khi đi LÊN (z tăng) ──
TRUNGGIAN_POINT_UP = {
    "x": 0.451, "y": 0.0, "z": 0.3,
    "qx": 0.964, "qy": 0.0, "qz": 0.266, "qw": 0.000,
    "order": [[2, 3], ["check_dir"]],
}

# ── Điểm trung gian khi đi XUỐNG (z giảm) ──
TRUNGGIAN_POINT_DOWN = {
    "x": 0.451, "y": 0.0, "z": 0.3,
    "qx": 0.007, "qy": 0.004, "qz": 0.000, "qw": 1.000,
    "order": [[2, 3], ["check_dir"]],
}

POINTS = [
    None,
    {
        "x": 0.242, "y": 0.007, "z": 0.607,
        "qx": 0.714, "qy": 0.008, "qz": 0.701, "qw": 0.008,
        "order": [[1], [2, 3, 4], ["close"]],
    },
    None,  
    {
        "x": 0.427, "y": -0.002, "z": 0.201,
        "qx": -0.012, "qy": -0.045, "qz": 0.001, "qw": 0.999,
        "order": [[1],[2, 3, 4], ["open"]],
    },
    None, 
    {
        "x": 0.07, "y": -0.0, "z": -0.081,
        "qx": -0.008, "qy": 0.736, "qz": -0.009, "qw": 0.677,
        "order": [[1], [2, 3, 4]],
    },
]

class ArmPubPoints(Node):
    def __init__(self):
        super().__init__('arm_pub_points')

        self.pub = self.create_publisher(String, '/arm_goal', 10)
        self.sub = self.create_subscription(JointState, '/joint_states', self.joint_callback, 10)
        self.ik_client = self.create_client(GetPositionIK, '/compute_ik')
        
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

        self.ik_client.wait_for_service()
        self.get_logger().info("[INIT] All Services READY")

        self.create_timer(0.1, self.tick)

    # ───────────── ROS CALLBACKS ─────────────
    def joint_callback(self, msg):
        try:
            joints = dict(zip(msg.name, msg.position))
            self.current_joints = [joints[j] for j in JOINT_NAMES]
        except Exception:
            pass

    # ───────────── TF HELPER ─────────────
    def get_current_tf(self):
        """Helper để lấy transform hiện tại, giúp code gọn hơn và tái sử dụng."""
        try:
            return self.tf_buffer.lookup_transform('world', 'end_effector_link', rclpy.time.Time())
        except Exception as e:
            # Chỉ log warn khi cần thiết để tránh trôi terminal
            return None

    def get_tf_q(self):
        t = self.get_current_tf()
        if t:
            q = t.transform.rotation
            return [q.x, q.y, q.z, q.w]
        return None

    # ───────────── GRIPPER CONTROL ─────────────
    def control_gripper(self, position, effort=1.0):
        goal = GripperCommand.Goal()
        goal.command.position = float(position)
        goal.command.max_effort = float(effort)

        self.get_logger().info(f"[GRIPPER] CMD → pos={position:.3f}, effort={effort}")
        send_future = self.gripper_client.send_goal_async(goal, feedback_callback=lambda _: None)
        send_future.add_done_callback(self.gripper_goal_response_cb)

    def gripper_goal_response_cb(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error("[GRIPPER] Goal rejected!")
            self.state = 'pause'
            return

        self.get_logger().info("[GRIPPER] Goal accepted")
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.gripper_result_cb)

    def gripper_result_cb(self, future):
        self.get_logger().info("[GRIPPER] DONE")
        self.step_idx += 1
        self.state = 'pause'
        self.pause_start = self.get_clock().now()

    # ───────────── MONITOR UP/DOWN ─────────────
    def monitor_direction(self):
        t = self.get_current_tf()
        if not t:
            return

        z = t.transform.translation.z
        x = t.transform.translation.x
        y = t.transform.translation.y

        if self.prev_z is not None:
            dz = z - self.prev_z
            if abs(dz) > DEAD_ZONE:
                direction = "↑ UP" if dz > 0 else "↓ DOWN"
                self.get_logger().info(f"[TF] {direction} | z={z:.4f}m dz={dz:+.4f} (x={x:.3f} y={y:.3f})")
            else:
                self.get_logger().info(f"[TF] ── HOLD | z={z:.4f}m (x={x:.3f} y={y:.3f})", throttle_duration_sec=1.0)
        self.prev_z = z

    # ───────────── SELECT TRUNGGIAN ─────────────
    def select_trunggian(self, trunggian_idx):
        next_real_idx = trunggian_idx + 1
        while next_real_idx < len(POINTS) and POINTS[next_real_idx] is None:
            next_real_idx += 1

        if next_real_idx >= len(POINTS):
            self.get_logger().warn(f"[PREDICT] Không tìm được điểm đích thực → fallback UP")
            POINTS[trunggian_idx] = TRUNGGIAN_POINT_UP
            return

        target_z = POINTS[next_real_idx]['z']
        t = self.get_current_tf()
        
        if not t:
            self.get_logger().warn(f"[PREDICT] TF error → fallback UP")
            POINTS[trunggian_idx] = TRUNGGIAN_POINT_UP
            return

        current_z = t.transform.translation.z
        dz = target_z - current_z

        if dz > 0:
            self.get_logger().info(f"[PREDICT] ↑ ĐI LÊN (z={current_z:.3f} → {target_z:.3f}) → TRUNGGIAN_UP")
            POINTS[trunggian_idx] = TRUNGGIAN_POINT_UP
        else:
            self.get_logger().info(f"[PREDICT] ↓ ĐI XUỐNG (z={current_z:.3f} → {target_z:.3f}) → TRUNGGIAN_DOWN")
            POINTS[trunggian_idx] = TRUNGGIAN_POINT_DOWN

    # ───────────── LOGIC: FLIP & CHECK ORIENTATION ─────────────
    def check_q_target(self):
        """
        Mục đích: Bắt buộc quay đế j1 hướng về phía (x, y) của điểm đích tiếp theo.
        Chỉ khi j1 quay xong thì mới trả về True để cho phép các khớp khác (j2, 3, 4) chạy.
        """
        if self.current_joints is None:
            return True

        # 1. Tìm điểm đích THỰC SỰ tiếp theo (bỏ qua TRUNGGIAN / None)
        next_real_idx = self.point_idx + 1
        while next_real_idx < len(POINTS) and POINTS[next_real_idx] is None:
            next_real_idx += 1

        if next_real_idx >= len(POINTS):
            return True

        target_pt = POINTS[next_real_idx]
        x = target_pt['x']
        y = target_pt['y']

        # 2. Tính góc j1 chuẩn cần đạt được để hướng về đích
        desired_j1 = math.atan2(y, x)
        # Chuẩn hóa góc về khoảng [-pi, pi]
        desired_j1 = math.atan2(math.sin(desired_j1), math.cos(desired_j1))

        current_j1 = self.current_joints[0]

        # 3. Tính độ lệch giữa j1 hiện tại và j1 cần thiết
        diff = abs(math.atan2(math.sin(desired_j1 - current_j1), math.cos(desired_j1 - current_j1)))

        self.get_logger().info(f"[CHECK DIR] j1 đang ở: {current_j1:.3f} | Cần quay tới: {desired_j1:.3f} | Lệch: {diff:.3f} rad")

        # 4. Nếu lệch quá 0.05 rad (~2.8 độ) thì BẮT BUỘC lật j1
        if diff > 0.05 and not self.flip_done:
            self.get_logger().warn(f"[FLIP] Cần quay mâm j1 trước để né thân robot...")
            self.flip_j1()
            self.flip_done = True
            return False  # Trả về False để State Machine dừng lại chờ j1 quay xong

        return True

    def flip_j1(self):
        if self.current_joints is None:
            return

        next_real_idx = self.point_idx + 1
        while next_real_idx < len(POINTS) and POINTS[next_real_idx] is None:
            next_real_idx += 1

        if next_real_idx >= len(POINTS):
            self.get_logger().warn("[FLIP] No next target → skip flip")
            return

        target_pt = POINTS[next_real_idx]
        x, y = target_pt['x'], target_pt['y']
        
        desired_j1 = math.atan2(y, x)
        desired_j1 = math.atan2(math.sin(desired_j1), math.cos(desired_j1))

        self.get_logger().warn(f"[FLIP] Quay theo target → atan2({y:.3f},{x:.3f}) = {desired_j1:.3f} rad")

        if self.ik_result:
            self.ik_result[0] = desired_j1

        target = list(self.current_joints)
        target[0] = desired_j1
        
        goal = { "x": 0, "y": 0, "z": 0, "j1": target[0], "j2": target[1], "j3": target[2], "j4": target[3] }
        self.pub.publish(String(data=json.dumps(goal)))
        
        self.target_step = target
        self.state = 'wait_arrive'

    # ───────────── IK ─────────────
    def compute_ik(self):
        pt = POINTS[self.point_idx]
        if pt is None:
            self.get_logger().error(f"[IK] POINTS[{self.point_idx}] là None! → skip")
            self.point_idx += 1
            self.state = 'wait_ready'
            return

        req = GetPositionIK.Request()
        req.ik_request = PositionIKRequest(group_name='arm', ik_link_name='end_effector_link')
        
        pose = PoseStamped()
        pose.header.frame_id = 'world'
        pose.pose.position.x, pose.pose.position.y, pose.pose.position.z = pt['x'], pt['y'], pt['z']
        pose.pose.orientation.x, pose.pose.orientation.y = pt['qx'], pt['qy']
        pose.pose.orientation.z, pose.pose.orientation.w = pt['qz'], pt['qw']
        req.ik_request.pose_stamped = pose

        if self.current_joints:
            js = JointState(name=JOINT_NAMES, position=self.current_joints)
            req.ik_request.robot_state = RobotState(joint_state=js)

        future = self.ik_client.call_async(req)
        future.add_done_callback(self.ik_callback)

    def ik_callback(self, future):
        res = future.result()
        if res.error_code.val != 1:
            self.get_logger().error("[IK] Fail → skip point")
            self.point_idx += 1
            self.state = 'wait_ready'
            return

        js = res.solution.joint_state
        d = dict(zip(js.name, js.position))
        self.ik_result = [d.get(j, 0) for j in JOINT_NAMES]

        self.get_logger().info(f"[IK] OK: {self.ik_result}")
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
        if self.current_joints is None:
            return

        self.monitor_direction()

        if self.state == 'go_home':
            goal = { "x": 0, "y": 0, "z": 0, "j1": 0, "j2": 0, "j3": 0, "j4": 0 }
            self.pub.publish(String(data=json.dumps(goal)))
            self.target_step = [0, 0, 0, 0]
            self.state = 'wait_home'

        elif self.state == 'wait_home':
            if self.arrived():
                self.state = 'wait_ready'

        elif self.state == 'wait_ready':
            self.flip_done = False
            if POINTS[self.point_idx] is None:
                self.select_trunggian(self.point_idx)
            self.compute_ik()
            self.state = 'wait_ik'

        elif self.state in ['wait_gripper', 'wait_ik']:
            pass # Chờ callbacks xử lý

        elif self.state == 'run_step':
            self.run_step()

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

                    if self.point_idx >= len(POINTS):
                        self.get_logger().info("[DONE] Finished all points!")
                        rclpy.shutdown()
                        return
                    self.state = 'wait_ready'
                else:
                    self.state = 'run_step'

def main():
    rclpy.init()
    node = ArmPubPoints()
    rclpy.spin(node)

if __name__ == '__main__':
    main()