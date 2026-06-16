import rclpy as rp
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import PoseStamped
# Nav2 Action 서버와 통신하기 위한 라이브러리
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
import math

class AutoExplorator(Node):
    def __init__(self):
        super().__init__('auto_explorator')
        
        # [이유] SLAM이 실시간으로 그리는 지도를 받아오기 위해 Subscriber 생성
        self.map_subscriber = self.create_subscription(OccupancyGrid, '/map', self.map_callback, 10)
            
        # [이유] 결정된 목적지를 Nav2 Action 서버로 보내 로봇을 움직이기 위해 Client 생성
        self.nav_action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        
        self.is_moving = False
        self.get_logger().info('터틀봇3 직접 짜는 자율 탐색 노드가 시작되었습니다.')

    def map_callback(self, msg):
        if self.is_moving:
            return

        # -----------------------------------------------------------------
        # [1단계] 1차원 지도 배열을 2차원(행렬) 공간 좌표로 변환
        # -----------------------------------------------------------------
        width = msg.info.width
        height = msg.info.height
        map_data = msg.data
        resolution = msg.info.resolution
        origin_x = msg.info.origin.position.x
        origin_y = msg.info.origin.position.y
        # 1차원 배열을 행과 열을 가진 2차원 공간 지도(Matrix)로 재정렬
        grid_map = [map_data[i * width:(i + 1) * width] for i in range(height)]

        # -----------------------------------------------------------------
        # [2단계] 프론티어(알고 있는 공간 '0'과 모르는 공간 '-1'의 경계선) 추출
        # -----------------------------------------------------------------
        frontiers = []
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                if grid_map[y][x] == 0:
                    if (grid_map[y+1][x] == -1 or grid_map[y-1][x] == -1 or 
                        grid_map[y][x+1] == -1 or grid_map[y][x-1] == -1):
                        
                        rx = x * resolution + origin_x
                        ry = y * resolution + origin_y
                        frontiers.append((rx, ry))

        # -----------------------------------------------------------------
        # [3단계] 검출된 수많은 경계점 중 최적의 목적지(Goal) 1개 선정
        # -----------------------------------------------------------------
        if not frontiers:
            self.get_logger().info('더 이상 갈 곳이 없습니다. 탐색 완료!')
            return

# 최단거리 프론티어 연산 로직 (로봇 중심 기준)
        robot_x = 0.0 
        robot_y = 0.0

        best_target = frontiers[0]
        min_distance = float('inf')

        for fx, fy in frontiers:
            distance = math.sqrt((fx - robot_x)**2 + (fy - robot_y)**2)
            if distance < min_distance and distance > 0.3:
                min_distance = distance
                best_target = (fx, fy)

        final_x, final_y = best_target
        self.send_goal_to_nav2(final_x, final_y)

    def send_goal_to_nav2(self, x, y):
        self.is_moving = True
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.orientation.w = 1.0

        self.get_logger().info(f'🎯 [타깃 전송] X: {x:.2f}m, Y: {y:.2f}m (최단거리: {math.sqrt(x**2+y**2):.2f}m)')
        
        self.nav_action_client.wait_for_server()
        send_goal_future = self.nav_action_client.send_goal_async(goal_msg)
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.is_moving = False
            return
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        self.get_logger().info('🏁 목적지 개척 완료. 맵 재분석을 시작합니다.')
        self.is_moving = False

def main(args=None):
    rp.init(args=args)
    node = AutoExplorator()
    rp.spin(node)
    node.destroy_node()
    rp.shutdown()

if __name__ == '__main__':
    main()
