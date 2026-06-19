import rclpy as rp
from rclpy.duration import Duration
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from geometry_msgs.msg import PoseStamped
import math
import time

def create_pose(navigator, x, y, yaw_degree):
    """X, Y 좌표와 각도(Degree)를 입력받아 Nav2용 PoseStamped 메시지를 만드는 함수"""
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()
    
    pose.pose.position.x = x
    pose.pose.position.y = y
    
    yaw_rad = math.radians(yaw_degree)
    pose.pose.orientation.z = math.sin(yaw_rad / 2.0)
    pose.pose.orientation.w = math.cos(yaw_rad / 2.0)
    
    return pose

def main():
    rp.init()
    nav = BasicNavigator()

    # 복귀할 홈 위치 정의
    home_pose = create_pose(nav, 0.0, 0.0, 0.0)

    # 배송할 목적지(A, B, C) 리스트
    delivery_targets = [
        {"name": "A 구역", "x": 1.0, "y": 0.0, "yaw": 0.0},
        {"name": "B 구역", "x": 1.5, "y": 1.0, "yaw": 90.0},
        {"name": "C 구역", "x": 0.0, "y": 1.5, "yaw": 180.0}
    ]

    print("\n[시작] 순차 배송 프로젝트를 시작합니다!")

    # 반복문을 돌며 A -> B -> C 순서대로 이동
    for target in delivery_targets:
        print(f"\n{target['name']}으로 배송을 시작합니다.")
        target_pose = create_pose(nav, target['x'], target['y'], target['yaw'])
        
        nav.goToPose(target_pose)
        
        # 이동 완료 대기
        while not nav.isTaskComplete():
            pass
            
        # 이동 결과 확인
        result = nav.getResult()
        if result == TaskResult.SUCCEEDED:
            print(f"{target['name']} 도착 완료! 물건 수령을 위해 5초간 대기합니다.")
            time.sleep(5.0)
        else:
            # 주행 실패 시 즉시 루프와 함수를 모두 빠져나갑니다 (함수 종료)
            print(f"\n[오류발생] {target['name']} 이동 중 실패했습니다! 시스템을 정지합니다.")
            print("배송 중 오류가 발생하여 안전을 위해 복귀하지 않고 현 위치에서 대기합니다.")
            return  # <--- 여기서 main() 함수를 바로 끝내버립니다!

    # ==================================================
    # For문을 무사히 통과했을 때만 아래 복귀 로직이 실행됩니다.
    # ==================================================
    print("\n========================================")
    print("모든 구역의 배송이 끝났습니다. 홈(Home)으로 복귀합니다.")
    print("========================================")
    
    nav.goToPose(home_pose)
    
    while not nav.isTaskComplete():
        pass
        
    if nav.getResult() == TaskResult.SUCCEEDED:
        print(" 홈 위치에 무사히 복귀했습니다. 모든 미션 성공!")
    else:
        print(" [오류발생] 복귀 중 문제가 발생했습니다. 수동 제어가 필요합니다.")

if __name__ == '__main__':
    main()
