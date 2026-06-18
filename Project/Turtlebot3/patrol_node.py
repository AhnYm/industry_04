import rclpy
from rclpy.duration import Duration
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from geometry_msgs.msg import PoseStamped
import math

def create_pose(navigator, x, y, yaw_degree):
    """X, Y 좌표와 각도(Degree)를 입력받아 Nav2용 PoseStamped 메시지를 만드는 함수"""
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()
    
    # 위치 설정 (미터 단위)
    pose.pose.position.x = x
    pose.pose.position.y = y
    
    # 각도 설정 (Degree를 오일러-쿼터니언 변환 변환)
    # 터틀봇이 평면(Z축 회전)만 움직이므로 간단히 계산
    yaw_rad = math.radians(yaw_degree)
    pose.pose.orientation.z = math.sin(yaw_rad / 2.0)
    pose.pose.orientation.w = math.cos(yaw_rad / 2.0)
    
    return pose

def main():
    rclpy.init()
    nav = BasicNavigator()

    # [중요] RViz2에서 '2D Pose Estimate'로 초기 위치를 지정했다면 
    # 아래 두 줄은 주석 해제(사용)하셔도 됩니다.
    # nav.waitUntilNav2Active()

    # 1. 순찰할 목적지 좌표들을 리스트로 정의
    # (실제 본인 맵의 RViz2 좌표를 보고 X, Y를 수정해야 합니다!)
    patrol_points = [
        create_pose(nav, 1.0, 0.5, 0.0),    # A 지점: X=1.0, Y=0.5, 정면(0도) 바라보기
        create_pose(nav, 0.0, 1.0, 90.0),   # B 지점: X=0.0, Y=1.0, 왼쪽(90도) 바라보기
        create_pose(nav, -0.5, 0.0, 180.0)  # C 지점: X=-0.5, Y=0.0, 뒤쪽(180도) 바라보기
    ]

    print("순찰 로봇 가동...!!")

    # 2. 무한 루프를 돌며 순찰
    while rclpy.ok():
        for i, point in enumerate(patrol_points):
            print(f"{i+1}번 목적지로 이동 중...")
            nav.goToPose(point)
            
            # 이동하는 동안 상태 모니터링 (도착할 때까지 대기)
            while not nav.isTaskComplete():
                feedback = nav.getFeedback()
                # 필요하면 여기서 피드백 데이터를 처리할 수 있습니다.
                
            # 결과 확인
            result = nav.getResult()
            if result == TaskResult.SUCCEEDED:
                print(f"{i+1}번 목적지 도착! 3초 대기 후 다음 지점으로 갑니다.")
                # 도착 후 잠시 대기 (물류 적재/순찰 가정)
                rclpy.spin_once(nav, timeout_sec=3.0) 
            else:
                print(f"{i+1}번 목적지 이동 실패 또는 취소됨. 다음 지점으로 건너뜁니다.")

if __name__ == '__main__':
    main()
