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
DEAD_ZONE = 0.001  # bỏ qua rung < 1mm

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
    {
        "x": 0.205, "y": 0.005, "z": 0.026,
        "qx": 0.000, "qy": 0.706, "qz": 0.000, "qw": 0.706,
        "order": [[1, 2, 3, 4], ["open"]],
    },
    None,  
    {
        "x": -0.05, "y": 0.000, "z": 0.547,
        "qx": -0.011, "qy": 0.016, "qz": 1.000, "qw": -0.000,
        "order": [[2, 3, 4], ["close"]],
    },
    None, 
    {
        "x": 0.184, "y": 0.031, "z": -0.061,
        "qx": 0.032, "qy": 0.672, "qz": 0.029, "qw": 0.739,
        "order": [[2,3,4], ["open"]],
    },
]


class ArmPubPoints(Node):
    def __init__(self):
        super().__init__('arm_pub_points')

        self.pub = self.create_publisher(String, '/arm_goal', 10)
        self.sub = self.create_subscription(JointState, '/joint_states', self.joint_callback, 10)
        self.ik_client = self.create_client(GetPositionIK, '/compute_ik')
        self.gripper_client = ActionClient(
            self,
            GripperCommand,
            '/gripper_controller/gripper_cmd'
        )

        self.gripper_client.wait_for_server()
        self.get_logger().info("Gripper action READY")
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.current_joints = None
        self.ik_result = None

        self.point_idx = 0
        self.step_idx = 0

        self.state = 'go_home'
        self.target_step = None
        self.pause_start = None

        self.flip_done = False

        # ── monitor UP/DOWN ──
        self.prev_z = None

        self.ik_client.wait_for_service()
        self.get_logger().info("READY")

        self.create_timer(0.1, self.tick)

    def joint_callback(self, msg):
        joints = dict(zip(msg.name, msg.position))
        try:
            self.current_joints = [joints[j] for j in JOINT_NAMES]
        except:
            pass
    #--------------- hàm điều khiển gipper-------------

    def control_gripper(self, position, effort=1.0):
        goal = GripperCommand.Goal()
        goal.command.position = float(position)
        goal.command.max_effort = float(effort)

        self.get_logger().info(
            f"Gripper CMD → pos={position:.3f}, effort={effort}"
        )

        send_future = self.gripper_client.send_goal_async(
            goal,
            feedback_callback=self.gripper_feedback_cb
        )
        send_future.add_done_callback(self.gripper_goal_response_cb)
    def gripper_goal_response_cb(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error("Gripper goal rejected")
            self.state = 'pause'
            return

        self.get_logger().info("Gripper goal accepted")

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.gripper_result_cb)


    def gripper_result_cb(self, future):
        self.get_logger().info("Gripper DONE")

        # 👉 CHỈ chuyển step ở đây (đợi kẹp xong)
        self.step_idx += 1
        self.state = 'pause'
        self.pause_start = self.get_clock().now()


    def gripper_feedback_cb(self, feedback):
        pass
    def gripper_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error("Gripper goal rejected")
            return

        self.get_logger().info("Gripper goal accepted")

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.gripper_result_callback)


    def gripper_result_callback(self, future):
        result = future.result().result
        self.get_logger().info("Gripper DONE")
    # ───────────── MONITOR UP/DOWN (reactive) ─────────────
    def monitor_direction(self):
        try:
            t = self.tf_buffer.lookup_transform(
                'world', 'end_effector_link', rclpy.time.Time()
            )
            z = t.transform.translation.z
            x = t.transform.translation.x
            y = t.transform.translation.y

            if self.prev_z is not None:
                dz = z - self.prev_z
                if abs(dz) > DEAD_ZONE:
                    direction = "↑ UP" if dz > 0 else "↓ DOWN"
                    self.get_logger().info(
                        f"{direction} | z={z:.4f}m  dz={dz:+.4f}  (x={x:.3f} y={y:.3f})"
                    )
                else:
                    self.get_logger().info(
                        f"── HOLD | z={z:.4f}m  (x={x:.3f} y={y:.3f})",
                        throttle_duration_sec=1.0
                    )

            self.prev_z = z

        except Exception as e:
            self.get_logger().warn(f"TF error: {e}", throttle_duration_sec=2.0)

    # ───────────── SELECT TRUNGGIAN (predictive) ─────────────
    def select_trunggian(self, trunggian_idx):
        """
        Dự đoán hướng dựa trên z hiện tại vs z điểm đích THỰC tiếp theo (bỏ qua None).
        Gán POINTS[trunggian_idx] = UP hoặc DOWN tương ứng.
        """
        # Tìm điểm đích thực SAU placeholder (bỏ qua các None liên tiếp nếu có)
        next_real_idx = trunggian_idx + 1
        while next_real_idx < len(POINTS) and POINTS[next_real_idx] is None:
            next_real_idx += 1

        if next_real_idx >= len(POINTS):
            self.get_logger().warn(
                f"[TRUNGGIAN idx={trunggian_idx}] Không tìm được điểm đích thực → fallback UP"
            )
            POINTS[trunggian_idx] = TRUNGGIAN_POINT_UP
            return

        target_z = POINTS[next_real_idx]['z']

        # Lấy z hiện tại từ TF
        try:
            t = self.tf_buffer.lookup_transform(
                'world', 'end_effector_link', rclpy.time.Time()
            )
            current_z = t.transform.translation.z
        except Exception as e:
            self.get_logger().warn(
                f"[TRUNGGIAN idx={trunggian_idx}] TF error: {e} → fallback UP"
            )
            POINTS[trunggian_idx] = TRUNGGIAN_POINT_UP
            return

        dz = target_z - current_z

        if dz > 0:
            self.get_logger().info(
                f"[PREDICT idx={trunggian_idx}] ↑ ĐI LÊN"
                f" (z={current_z:.3f} → {target_z:.3f}, dz={dz:+.3f})"
                f" → TRUNGGIAN_UP"
            )
            POINTS[trunggian_idx] = TRUNGGIAN_POINT_UP
        else:
            self.get_logger().info(
                f"[PREDICT idx={trunggian_idx}] ↓ ĐI XUỐNG"
                f" (z={current_z:.3f} → {target_z:.3f}, dz={dz:+.3f})"
                f" → TRUNGGIAN_DOWN"
            )
            POINTS[trunggian_idx] = TRUNGGIAN_POINT_DOWN

    # ───────────── TF quaternion ─────────────
    def get_tf_q(self):
        try:
            t = self.tf_buffer.lookup_transform('world', 'end_effector_link', rclpy.time.Time())
            q = t.transform.rotation
            return [q.x, q.y, q.z, q.w]
        except:
            return None
    def check_q_target(self):
        q_current = self.get_tf_q()
        if q_current is None:
            return True

        pt = POINTS[self.point_idx]
        q_target = [pt['qx'], pt['qy'], pt['qz'], pt['qw']]

        dot = sum(q_target[i] * q_current[i] for i in range(4))

        self.get_logger().info(f"Q dot target = {dot:.3f}")

        if dot < 0.7 and not self.flip_done:
            self.get_logger().warn(f"Sai orientation (dot={dot:.3f}) → thử flip j1")
            self.flip_j1()
            self.flip_done = True
            return False

        return True   # ← THIẾU CÁI NÀY
    # ───────────── CHECK TOOL DIRECTION ─────────────
    def check_direction(self):
        q = self.get_tf_q()
        if q is None:
            return True

        x, y, z, w = q

        # Trục Z của tool trong frame world
        z_axis = [
            2 * (x * z + y * w),
            2 * (y * z - x * w),
            1 - 2 * (x * x + y * y)
        ]

        target_dir = [0, 0, -1]
        dot = sum(z_axis[i] * target_dir[i] for i in range(3))

        # Xác định hướng di chuyển: tìm điểm đích thực SAU trung gian hiện tại
        next_real_idx = self.point_idx + 1
        while next_real_idx < len(POINTS) and POINTS[next_real_idx] is None:
            next_real_idx += 1

        going_down = False
        if next_real_idx < len(POINTS):
            try:
                t = self.tf_buffer.lookup_transform(
                    'world', 'end_effector_link', rclpy.time.Time()
                )
                current_z = t.transform.translation.z
                target_z = POINTS[next_real_idx]['z']
                going_down = (target_z - current_z) < 0
            except:
                pass

        direction_str = "XUONG" if going_down else "LEN"

        # Kiem tra j1 co dung goc phan tu khong:
        # Di LEN  : j1 ~ 0   -> |j1| < pi/2
        # Di XUONG: j1 ~ +/-pi -> |j1| > pi/2
        j1 = self.current_joints[0]
        j1_ok_for_down = abs(j1) > (math.pi / 2)
        j1_ok_for_up   = abs(j1) < (math.pi / 2)

        self.get_logger().info(
            f"Z align = {dot:.3f}  j1 = {j1:.3f}rad  (huong di: {direction_str})"
        )

        need_flip = False

        if going_down:
            if dot < -0.7:
                self.get_logger().warn("Di XUONG: tool huong nguoc (dot < -0.7) -> flip")
                need_flip = True
            elif not j1_ok_for_down:
                self.get_logger().warn(
                    f"Di XUONG: dot OK ({dot:.3f}) nhung j1={j1:.3f} chua dung goc phan tu -> flip"
                )
                need_flip = True
        else:
            if dot < -0.7:
                self.get_logger().warn("Di LEN: tool huong nguoc (dot < -0.7) -> flip")
                need_flip = True
            elif not j1_ok_for_up:
                self.get_logger().warn(
                    f"Di LEN: dot OK ({dot:.3f}) nhung j1={j1:.3f} chua dung goc phan tu -> flip"
                )
                need_flip = True

        if need_flip and not self.flip_done:
            self.flip_j1()
            self.flip_done = True
            return False

        return dot > 0.7

    # ───────────── FLIP J1 ─────────────
    def flip_j1(self):
        current = self.current_joints[0]

        new = current + math.pi
        if new > math.pi:
            new -= 2 * math.pi

        self.get_logger().warn(f"Flip j1: {current:.3f} → {new:.3f}")

        target = list(self.current_joints)
        target[0] = new

        goal = {
            "x": 0, "y": 0, "z": 0,
            "j1": target[0], "j2": target[1],
            "j3": target[2], "j4": target[3],
        }

        self.pub.publish(String(data=json.dumps(goal)))
        self.target_step = target
        self.state = 'wait_arrive'

    # ───────────── IK ─────────────
    def compute_ik(self):
        pt = POINTS[self.point_idx]

        # Guard: không bao giờ gọi IK khi point vẫn là None
        if pt is None:
            self.get_logger().error(
                f"POINTS[{self.point_idx}] vẫn là None khi compute_ik! → skip"
            )
            self.point_idx += 1
            self.state = 'wait_ready'
            return

        req = GetPositionIK.Request()
        req.ik_request = PositionIKRequest()
        req.ik_request.group_name = 'arm'
        req.ik_request.ik_link_name = 'end_effector_link'

        pose = PoseStamped()
        pose.header.frame_id = 'world'
        pose.pose.position.x = pt['x']
        pose.pose.position.y = pt['y']
        pose.pose.position.z = pt['z']
        pose.pose.orientation.x = pt['qx']
        pose.pose.orientation.y = pt['qy']
        pose.pose.orientation.z = pt['qz']
        pose.pose.orientation.w = pt['qw']

        req.ik_request.pose_stamped = pose

        rs = RobotState()
        if self.current_joints:
            js = JointState()
            js.name = JOINT_NAMES
            js.position = self.current_joints
            rs.joint_state = js

        req.ik_request.robot_state = rs

        future = self.ik_client.call_async(req)
        future.add_done_callback(self.ik_callback)

    def ik_callback(self, future):
        res = future.result()

        if res.error_code.val != 1:
            self.get_logger().error("IK fail → skip point")
            self.point_idx += 1
            self.state = 'wait_ready'
            return

        js = res.solution.joint_state
        d = dict(zip(js.name, js.position))
        self.ik_result = [d.get(j, 0) for j in JOINT_NAMES]

        self.get_logger().info(f"IK OK: {self.ik_result}")

        self.state = 'run_step'

    # ───────────── STEP ─────────────
    def run_step(self):
        pt = POINTS[self.point_idx]
        order = pt['order']
        group = order[self.step_idx]
        if group == ["close"]:
            self.control_gripper(0.0, effort=3.0)   # đóng nhẹ thôi
            self.state = 'wait_gripper'
            return

        if group == ["open"]:
            self.control_gripper(0.01, effort=1.0)  # mở nhẹ
            self.state = 'wait_gripper'
            return
        if group == ["check_dir"]:
            if not self.check_q_target():
                return

            self.step_idx += 1
            self.state = 'pause'
            self.pause_start = self.get_clock().now()
            return

        if self.ik_result is None:
            return

        target = list(self.current_joints)

        for j in group:
            target[j - 1] = self.ik_result[j - 1]

        goal = {
            "x": pt['x'], "y": pt['y'], "z": pt['z'],
            "j1": target[0], "j2": target[1],
            "j3": target[2], "j4": target[3],
        }

        self.pub.publish(String(data=json.dumps(goal)))
        self.target_step = target
        self.state = 'wait_arrive'

    # ───────────── CHECK ARRIVED ─────────────
    def arrived(self):
        if self.target_step is None:
            return False
        err = [abs(self.target_step[i] - self.current_joints[i]) for i in range(4)]
        return max(err) < ARRIVE_THRESHOLD

    # ───────────── MAIN LOOP ─────────────
    def tick(self):
        if self.current_joints is None:
            return

        # gọi monitor mỗi tick
        self.monitor_direction()

        if self.state == 'go_home':
            self.pub.publish(String(data=json.dumps({
                "x": 0, "y": 0, "z": 0, "j1": 0, "j2": 0, "j3": 0, "j4": 0
            })))
            self.target_step = [0, 0, 0, 0]
            self.state = 'wait_home'

        elif self.state == 'wait_home':
            if self.arrived():
                self.state = 'wait_ready'

        elif self.state == 'wait_ready':
            self.flip_done = False

            # ── Nếu điểm hiện tại là placeholder None → chọn UP/DOWN trước khi IK ──
            if POINTS[self.point_idx] is None:
                self.select_trunggian(self.point_idx)

            self.compute_ik()
            self.state = 'wait_ik'
        elif self.state == 'wait_gripper':
            return
        elif self.state == 'wait_ik':
            return

        elif self.state == 'run_step':
            self.run_step()

        elif self.state == 'wait_arrive':
            if self.arrived():
                self.step_idx += 1
                self.state = 'pause'
                self.pause_start = self.get_clock().now()

        elif self.state == 'pause':
            t = (self.get_clock().now() - self.pause_start).nanoseconds / 1e9
            if t > PAUSE_BETWEEN:
                order = POINTS[self.point_idx]['order']

                if self.step_idx >= len(order):
                    self.point_idx += 1
                    self.step_idx = 0
                    self.ik_result = None

                    if self.point_idx >= len(POINTS):
                        self.get_logger().info("DONE")
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