import rclpy as rp
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import PoseStamped
# Nav2 Action 서버와 통신하기 위한 라이브러리
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose

class AutoExplorator(Node):
    def __init__(self):
        super().__init__('auto_explorator')
        
        # [이유] SLAM이 실시간으로 그리는 지도를 받아오기 위해 Subscriber 생성
        self.map_subscriber = self.create_subscription(OccupancyGrid, '/map', self.map_callback, 10)
            
        # [이유] 결정된 목적지를 Nav2 Action 서버로 보내 로봇을 움직이기 위해 Client 생성
        self.nav_action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        
        self.latest_map = None
        self.get_logger().info('터틀봇3 직접 짜는 자율 탐색 노드가 시작되었습니다.')

    def map_callback(self, msg):
        """ SLAM으로부터 실시간 지도가 들어올 때마다 실행되는 함수 """
        self.latest_map = msg
        # 지도가 들어오면 자동 탐색 알고리즘 루프 실행
        self.run_exploration_loop()

    def run_exploration_loop(self):
        if self.latest_map is None:
            return

        # -----------------------------------------------------------------
        # [1단계] 1차원 지도 배열을 2차원(행렬) 공간 좌표로 변환
        # -----------------------------------------------------------------
        width = self.latest_map.info.width
        height = self.latest_map.info.height
        map_data = self.latest_map.data  # 1차원 리스트 형태 (-1, 0, 100으로 구성됨)
        
        # 1차원 배열을 행과 열을 가진 2차원 공간 지도(Matrix)로 재정렬
        grid_map = [map_data[i * width:(i + 1) * width] for i in range(height)]

        # -----------------------------------------------------------------
        # [2단계] 프론티어(알고 있는 공간 '0'과 모르는 공간 '-1'의 경계선) 추출
        # -----------------------------------------------------------------
        frontiers = []
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                # 내가 있는 칸이 안전구역(0)이고
                if grid_map[y][x] == 0:
                    # 상하좌우 이웃한 칸 중에 미지 구역(-1)이 하나라도 있다면?
                    if (grid_map[y+1][x] == -1 or grid_map[y-1][x] == -1 or 
                        grid_map[y][x+1] == -1 or grid_map[y][x-1] == -1):
                        # 그곳이 바로 탐색해야 할 '경계점(Frontier)'입니다.
                        frontiers.append((x, y))

        # -----------------------------------------------------------------
        # [3단계] 검출된 수많은 경계점 중 최적의 목적지(Goal) 1개 선정
        # -----------------------------------------------------------------
        if not frontiers:
            self.get_logger().info('더 이상 갈 곳이 없습니다. 탐색 완료!')
            return

        # [우선순위 로직 기획 내용]
        # 계산 편의상 가장 먼저 발견된 첫 번째 경계점을 목적지로 임시 설정합니다.
        # (실제 고도화 단계에서는 '로봇과 가장 가까운 점'을 수학적 거리 공식으로 연산하여 고릅니다.)
        target_grid_x, target_grid_y = frontiers[0]

        # 픽셀(격자) 주소를 실제 로봇이 다니는 현실 세계 좌표(미터 단위)로 변환합니다.
        resolution = self.latest_map.info.resolution  # 격자 한 칸의 실제 크기 (예: 0.05m)
        origin_x = self.latest_map.info.origin.position.x
        origin_y = self.latest_map.info.origin.position.y

        real_world_x = target_grid_x * resolution + origin_x
        real_world_y = target_grid_y * resolution + origin_y

        # -----------------------------------------------------------------
        # [4단계] 선정된 좌표를 Nav2 명령으로 전송하여 로봇 이동시키기
        # -----------------------------------------------------------------
        self.send_goal(real_world_x, real_world_y)

    def send_goal(self, x, y):
        # Nav2가 알아듣는 Action Goal 메시지 형식에 맞춰 데이터 포장
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        
        # Action 서버가 준비되었는지 확인 후 목적지 전송
        self.nav_action_client.wait_for_server()
        self.nav_action_client.send_goal_async(goal_msg)
        self.get_logger().info(f'새로운 탐색 목적지 발송 완료: X={x:.2f}, Y={y:.2f}')

def main(args=None):
    rp.init(args=args)
    node = AutoExplorator()
    rp.spin(node)
    node.destroy_node()
    rp.shutdown()

if __name__ == '__main__':
    main()
