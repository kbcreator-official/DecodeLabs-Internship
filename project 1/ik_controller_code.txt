import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import Constraints, PositionConstraint
from geometry_msgs.msg import Pose
from shape_msgs.msg import SolidPrimitive

class PandaIKController(Node):
    def __init__(self):
        super().__init__('panda_ik_controller')
        self._action_client = ActionClient(self, MoveGroup, '/move_action')
        self.get_logger().info('Panda IK Controller Ready!')
        self.timer = self.create_timer(2.0, self.send_goal)

    def send_goal(self):
        self.timer.cancel()
        goal_msg = MoveGroup.Goal()
        goal_msg.request.group_name = 'panda_arm'
        goal_msg.request.num_planning_attempts = 10
        goal_msg.request.allowed_planning_time = 10.0
        goal_msg.request.max_velocity_scaling_factor = 0.1
        goal_msg.request.max_acceleration_scaling_factor = 0.1

        target_pose = Pose()
        target_pose.position.x = 0.3
        target_pose.position.y =0.0
        target_pose.position.z = 0.4
        target_pose.orientation.w = 1.0

        pos_constraint = PositionConstraint()
        pos_constraint.header.frame_id = 'panda_link0'
        pos_constraint.link_name = 'panda_hand'
        primitive = SolidPrimitive()
        primitive.type = SolidPrimitive.SPHERE
        primitive.dimensions = [0.2]
        pos_constraint.constraint_region.primitives.append(primitive)
        pos_constraint.constraint_region.primitive_poses.append(target_pose)
        pos_constraint.weight = 1.0

        constraints = Constraints()
        constraints.position_constraints.append(pos_constraint)
        goal_msg.request.goal_constraints.append(constraints)

        self.get_logger().info('Waiting for server...')
        self._action_client.wait_for_server()
        self.get_logger().info('Sending goal...')
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal REJECTED!')
            return
        self.get_logger().info('Goal ACCEPTED! Planning...')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        result = future.result().result
        if result.error_code.val == 1:
            self.get_logger().info('SUCCESS! Arm moved to target!')
        else:
            self.get_logger().error(f'FAILED! Error: {result.error_code.val}')

def main(args=None):
    rclpy.init(args=args)
    node = PandaIKController()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
