import rclpy as rp
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
    
    # 각도(Degree)를 쿼터니언으로 변환
    # 터틀봇이 평면(Z축 회전)만 움직이므로 간단히 계산
    yaw_rad = math.radians(yaw_degree)
    pose.pose.orientation.z = math.sin(yaw_rad / 2.0)
    pose.pose.orientation.w = math.cos(yaw_rad / 2.0)
    
    return pose

def main():
    rp.init()
    nav = BasicNavigator()

    target_pose = create_pose(nav, 1.0, 0.0, 0.0)  # 내가 지정한 1구역 위치
    home_pose = create_pose(nav, 0.0, 0.0, 0.0)    # 처음 출발한 원점 위치

    print("\n1구역 배송을 시작합니다!")

    # ==================================================
    # 1단계: 지정한 1구역으로 이동
    # ==================================================
    print("1구역으로 이동 중...")
    nav.goToPose(target_pose)
    
    # 도착할 때까지 무한 대기하며 상태 모니터링
    while not nav.isTaskComplete():
        pass
        
    # 이동 결과 확인
    result = nav.getResult()
    if result == TaskResult.SUCCEEDED:
        print("1구역 도착 완료! 물건을 내리기 위해 5초간 대기합니다.")
        time.sleep(5.0)  # 5초 대기
    else:
        print("1구역 이동 실패! 복귀를 시도합니다.")

    # ==================================================
    # 2단계: 원래 자리(Home)로 복귀
    # ==================================================
    print("\n배송 완료! 원래 자리(Home)로 복귀합니다.")
    nav.goToPose(home_pose)
    
    while not nav.isTaskComplete():
        pass
        
    if nav.getResult() == TaskResult.SUCCEEDED:
        print("홈 위치에 무사히 복귀했습니다! 초안 테스트 성공!")
    else:
        print("복귀 중 문제가 발생했습니다.")

if __name__ == '__main__':
    main()
