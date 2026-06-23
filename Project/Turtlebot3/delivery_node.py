import rclpy as rp  # ROS 2 Python 클라이언트 라이브러리 임포트
from rclpy.duration import Duration  # 시간 간격을 다루기 위한 Duration 클래스 임포트
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult  # Nav2 내비게이션 제어 및 결과 확인을 위한 클래스 임포트
from geometry_msgs.msg import PoseStamped  # 로봇의 위치와 방향 정보를 담는 메시지 타입 임포트
import math  # 오일러 각도를 라디안으로 변환하기 위한 수학 라이브러리 임포트
import time  # 대기 시간 지연을 위한 time 라이브러리 임포트

def create_pose(navigator, x, y, yaw_degree):
    """X, Y 좌표와 각도(Degree)를 입력받아 Nav2용 PoseStamped 메시지를 만드는 함수"""
    pose = PoseStamped()  # 위치 정보를 담을 객체 생성
    pose.header.frame_id = 'map'  # 기준 좌표계를 절대 좌표계인 'map'으로 설정
    pose.header.stamp = navigator.get_clock().now().to_msg()  # 현재 로봇 시스템의 실시간 타임스탬프 기록
    
    pose.pose.position.x = x  # 입력받은 X축 위치 대입 (미터 단위)
    pose.pose.position.y = y  # 입력받은 Y축 위치 대입 (미터 단위)
    
    yaw_rad = math.radians(yaw_degree)  # 가독성 좋은 도(Degree) 단위를 수학 연산용 라디안(Radian)으로 변환
    pose.pose.orientation.z = math.sin(yaw_rad / 2.0)  # 평면 2D 회전을 위한 쿼터니언 Z값 계산 및 대입
    pose.pose.orientation.w = math.cos(yaw_rad / 2.0)  # 평면 2D 회전을 위한 쿼터니언 W값 계산 및 대입
    
    return pose  # 완성된 위치 및 방향 데이터 반환

def main():
    rp.init()  # ROS 2 통신을 위한 초기화 수행
    nav = BasicNavigator()  # Nav2 내비게이션 명령을 내릴 제어 객체 생성

    # 1. 각 구간별 주행 경로 (경유지들 + 최종 목적지) 설정 단계
    
    # 1) 홈 -> C구역 이동 경로 데이터 정의
    waypoints_to_C = [
        create_pose(nav, 1.754, 0.005, 0.0),    # 갈림길 우회를 위한 첫 번째 고정 경유지
        create_pose(nav, 1.824, 0.422, 90.0),   # 두 번째 고정 경유지
        create_pose(nav, 1.094, 0.486, -179.2), # 세 번째 고정 경유지
    ]   
    goal_C = create_pose(nav, 1.366, 1.132, 9.3)     # C구역 배송 최종 정지 목적지

    # 2) C구역 -> A구역 이동 경로 데이터 정의
    waypoints_to_A = [
        create_pose(nav, 1.136, 1.150, -177.0),  # C구역 출발 직후 거쳐갈 경유지 1
        create_pose(nav, 0.945, 0.445, -91.2),   # 경유지 2
        create_pose(nav, 0.647, 1.886 , 91.8),   # 경유지 3
    ]
    goal_A = create_pose(nav, 0.091, 2.265, 178.0)   # A구역 배송 최종 정지 목적지

    # 3) A구역 -> B구역 이동 경로 데이터 정의
    waypoints_to_B = [create_pose(nav, 0.767, 1.855 , 9.0)] # B구역 진입 전 좁은 길목 제어를 위한 경유지
    goal_B = create_pose(nav, 1.370, 1.431, 0.0)   # B구역 배송 최종 정지 목적지
 
    # 4) B구역 -> 홈(Home) 복귀 경로 데이터 정의
    waypoints_to_home = [
        create_pose(nav, 0.587, 0.895, 170.0),  # 안전한 원점 복귀를 위한 경유지 1
        create_pose(nav, 0.214, 0.036, -115),   # 경유지 2
        create_pose(nav, -0.203, 0.366, 150)    # 경유지 3
    ]
    goal_home = create_pose(nav, -0.723, -0.578, 0)    # 출발지 원점(Home) 최종 정지 목적지

    # 순차 배송 태스크 데이터를 딕셔너리 리스트 구조로 체계화
    delivery_tasks = [
        {"name": "C 구역", "waypoints": waypoints_to_C, "goal": goal_C},
        {"name": "A 구역", "waypoints": waypoints_to_A, "goal": goal_A},
        {"name": "B 구역", "waypoints": waypoints_to_B, "goal": goal_B}
    ]

    print("\n지정 경로 순차 배송를 시작합니다.")

    # 2. 고정 경로를 따라 순차 배송 루프 제어 시작
    for task in delivery_tasks:
        print(f"\n지정된 경로를 통해 {task['name']}(으)로 이동을 시작합니다.")
        
        # 지정한 구역의 경유지 리스트를 한 번에 전달하여 연속 주행 명령 하달
        nav.followWaypoints(task["waypoints"])
        time.sleep(0.5)  # Nav2 액션 서버의 상태 전환 및 버퍼링 시간 보장
        
        # 경유지 리스트 주행이 끝날 때까지 무한 대기
        while not nav.isTaskComplete():
            time.sleep(0.1)  # CPU 과부하 방지를 위한 미세 대기 시간 설정
            
        # 경유지 주행 완료 결과 확인
        if nav.getResult() != TaskResult.SUCCEEDED:
            print(f"\n{task['name']} 경유지 주행 중 오류가 발생했습니다. 시스템을 정지합니다.")
            return  # 미션 실패 시 아래 로직을 타지 않고 즉시 프로그램 완전 정지(종료)

        # 경유지를 성공적으로 다 통과했다면 최종 종착지로 안내
        print(f"{task['name']} 최종 목적지에 진입합니다.")
        nav.goToPose(task["goal"])  # 정밀 정지 및 회전 정렬을 위해 goToPose 단독 명령 수행
        time.sleep(0.5)  # 명령 인식 시간 제공
        
        # 최종 목적지 정지 완료 시점까지 대기
        while not nav.isTaskComplete():
            time.sleep(0.1)

        # 최종 정지 성공 여부 검사
        if nav.getResult() == TaskResult.SUCCEEDED:
            print(f"{task['name']} 최종 목적지에 완전히 정지했습니다. 물건 수령을 위해 5초간 대기합니다.")
            time.sleep(5.0)  # 시나리오에 따른 배송 시간 5초간 정지 대기
        else:
            print(f"\n{task['name']} 최종 목적지 진입 중 오류가 발생했습니다. 시스템을 정지합니다.")
            return  # 목적지 진입 실패 시에도 복귀하지 않고 즉시 강제 종료

    # [복귀 단계] 모든 루프가 에러 없이 성공(for문 통과) 시 실행되는 파트
    print("\n===============================================================")
    print("모든 구역의 배송이 끝났습니다. 복귀 경로를 통해 홈으로 이동합니다.")
    print("===============================================================")
    
    # 홈 복귀 단계 1: 지정된 복귀용 경유지 리스트 주행 명령
    nav.followWaypoints(waypoints_to_home)
    time.sleep(0.5)  # 타이밍 완충 대기
    while not nav.isTaskComplete():
        time.sleep(0.1)
        
    # 복귀 주행 중 에러 검사
    if nav.getResult() != TaskResult.SUCCEEDED:
        print("복귀 경유지 주행 중 문제가 발생했습니다.")
        return  # 에러 발생 시 원점 진입 시도를 중단하고 정지

    # 홈 복귀 단계 2: 최종 충전/정비 원점에 완벽히 안착 정지
    nav.goToPose(goal_home)
    time.sleep(0.5)
    while not nav.isTaskComplete():
        time.sleep(0.1)
        
    # 최종 원점 안착 성공 여부 판정
    if nav.getResult() == TaskResult.SUCCEEDED:
        print("홈 위치에 지정 경로로 무사히 복귀했습니다. 모든 미션을 마칩니다.")
    else:
        print("홈 최종 복귀 주행 중 문제가 발생했습니다. 수동 제어가 필요합니다.")

if __name__ == '__main__':
    main()  # 스크립트 실행 시 메인 함수 호출
