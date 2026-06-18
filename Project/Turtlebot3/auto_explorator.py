import rclpy as rp
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import PoseStamped
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus
import math

class AutoExplorator(Node):
    def __init__(self):
        super().__init__('auto_explorator')
        
        self.map_subscriber = self.create_subscription(OccupancyGrid, '/map', self.map_callback, 10)
        self.nav_action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        
        self.is_moving = False
        
        # 로봇 주행 기준점
        self.current_robot_x = 0.0
        self.current_robot_y = 0.0
        
        # 블랙리스트 기록 리스트
        self.blacklisted_targets = []
        
        self.get_logger().info('⚡ [좁은 공간 돌파 튜닝 완료] 자율 탐색 노드가 시작되었습니다.')

    def map_callback(self, msg):
        if self.is_moving:
            return
            
        width = msg.info.width
        height = msg.info.height
        map_data = msg.data
        resolution = msg.info.resolution
        origin_x = msg.info.origin.position.x
        origin_y = msg.info.origin.position.y
        
        grid_map = [map_data[i * width:(i + 1) * width] for i in range(height)]
        
        frontiers = []
        for y in range(3, height - 3, 3):
            for x in range(3, width - 3, 3):
                if grid_map[y][x] == 0:
                    if (grid_map[y+1][x] == -1 or grid_map[y-1][x] == -1 or 
                        grid_map[y][x+1] == -1 or grid_map[y][x-1] == -1):
                        
                        # 🛠️ [핵심 수정] 벽면 필터 조사 반경을 3칸에서 1칸으로 축소!
                        # 좁은 통로 틈새에 끼어있는 경계선 픽셀들이 억울하게 필터링되는 현상을 방지합니다.
                        has_wall_nearby = False
                        for ny in range(y - 1, y + 2):
                            for nx in range(x - 1, x + 2):
                                if grid_map[ny][nx] >= 60: # 벽 판단 기준 확률도 60으로 상향 유연화
                                    has_wall_nearby = True
                                    break
                            if has_wall_nearby:
                                break
                        
                        if not has_wall_nearby:
                            rx = x * resolution + origin_x
                            ry = y * resolution + origin_y
                            
                            # 🛠️ [핵심 수정] 블랙리스트 필터 반경을 0.45m에서 0.25m로 축소!
                            # 좁은 구역 안에 갇혀서 주변 대안 좌표들까지 블랙리스트에 묶여 증발하는 문제를 해결합니다.
                            is_blacklisted = False
                            for bx, by in self.blacklisted_targets:
                                if math.sqrt((rx - bx)**2 + (ry - by)**2) < 0.25:
                                    is_blacklisted = True
                                    break
                            
                            if not is_blacklisted:
                                frontiers.append((rx, ry))
                        
        if not frontiers:
            self.get_logger().warn('🔍 갈 수 있는 공간이나 경계선이 일시적으로 보이지 않아 블랙리스트를 완전 리셋합니다.')
            self.blacklisted_targets.clear()
            return

        # 최단거리 타깃 선정
        best_target = frontiers[0]
        min_distance = float('inf')

        for fx, fy in frontiers:
            distance = math.sqrt((fx - self.current_robot_x)**2 + (fy - self.current_robot_y)**2)
            if 0.3 < distance < min_distance: # 단거리 진입 한계를 0.4에서 0.3으로 완화
                min_distance = distance
                best_target = (fx, fy)

        target_x, target_y = best_target
        
        # 최근 5개의 원본 목적지만 블랙리스트로 타이트하게 관리
        self.blacklisted_targets.append((target_x, target_y))
        if len(self.blacklisted_targets) > 5:
            self.blacklisted_targets.pop(0)
        
        # ⚠️ [물리 제약 한계선 공식] 로봇 기준 1.3m 이내로 축소
        dx = target_x - self.current_robot_x
        dy = target_y - self.current_robot_y
        final_dist = math.sqrt(dx**2 + dy**2)
        
        MAX_ALLOWED_DIST = 1.3
        if final_dist > MAX_ALLOWED_DIST:
            ratio = MAX_ALLOWED_DIST / final_dist
            final_x = self.current_robot_x + dx * ratio
            final_y = self.current_robot_y + dy * ratio
        else:
            final_x = target_x
            final_y = target_y

        self.send_goal_to_nav2(final_x, final_y)

    def send_goal_to_nav2(self, x, y):
        self.is_moving = True

        self.current_robot_x = x
        self.current_robot_y = y

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.orientation.w = 1.0

        self.get_logger().info(f'🎯 [목적지 전송] X: {x:.2f}m, Y: {y:.2f}m')
        
        self.nav_action_client.wait_for_server()
        send_goal_future = self.nav_action_client.send_goal_async(goal_msg)
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn('❌ [목적지 거절] 진입 불가 구역입니다.')
            self.is_moving = False
            return

        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        action_result = future.result()
        
        if action_result.status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('🏁 목적지 도달 성공.')
        else:
            self.get_logger().error('🚨 주행 실패 또는 우회 처리 진행.')
            
        self.is_moving = False

def main(args=None):
    rp.init(args=args)
    node = AutoExplorator()
    rp.spin(node)
    node.destroy_node()
    rp.shutdown()

if __name__ == '__main__':
    main()
