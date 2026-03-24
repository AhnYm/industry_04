import cv2
import random
import pygame
import time

class Ball:
    def __init__(self):
        super().__init__()
        print("A ball object created")
        self.radius=0
        # 은닉도 가능
        (self.x,self.y)=(0,0)
        self.is_activate=False
    def __del__(self):
        print("A ball object deleted")

# 랜덤한 위치를 생성하는 함수
def get_random_position(frame_width,frame_height,radius) -> tuple:
    x = random.randint(radius,frame_width - radius) #x축 범위
    y = random.randint(radius, frame_height - radius) #y축 범위
    return x,y

#코인 그리기 함수
def draw_coin(img, center, radius):
    center_x = int(center[0])
    center_y = int(center[1])
    # 금색 테두리 (가장 바깥쪽)
    cv2.circle(img, (center_x, center_y), radius, (0, 165, 255), -1)
    # 노란색 몸체
    cv2.circle(img, (center_x, center_y), int(radius * 0.85), (0, 255, 255), -1)
    # 가운데 'C' 글자(반지름 비례해서 계산)
    font_scale=max(0.1, radius/30.0)  #최소 0.1보장
    text_position =(int(center_x - radius*0.4), int(center_y + radius*0.4))
    cv2.putText(img, "C", text_position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 165, 255), 2)

def main() -> None:
    pygame.mixer.init()

    # 배경음악 로드
    try:
        pygame.mixer.music.load("bgm.mp3")
        pygame.mixer.music.set_volume(0.5)
        # pygame.mixer.music.play(-1)  #무한 반복
    except:
        print("경고: bgm.mp3 파일을 찾을 수 없습니다.")
    # 효과음 로드
    try:
        hit_sound = pygame.mixer.Sound("hit.wav")
        hit_sound.set_volume(0.3)  # 30%로 설정
    except:
        hit_sound = None
        print("경고: hit.wav 파일을 찾을 수 없습니다.")
    #카운트다운용 소리
    try:
        count_sound = pygame.mixer.Sound("count.wav")
        count_sound.set_volume(0.6)
    except:
        hit_sound = None
        print("경고: count.wav 파일을 찾을 수 없습니다.")

    capture=cv2.VideoCapture(0) # 지정 카메라 작동
    if not capture.isOpened():
        print("Cannot open camera")
    # 화면의 크기를 가져오기
    frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))  # 캡의 폭을 받아 적용
    frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)) # 캡의 높이을 받아 적용
    print(f"W : {frame_width}, H: {frame_height}")

    # 코인의 객체화 및 초기화
    coin=Ball() # 생성자 호출 -> 객체화
    coin.radius=20 # 15픽셀
    (coin.x,coin.y)=get_random_position(frame_width,frame_height,coin.radius)
    coin.is_activate = True

    score=0 # 점수를 저장하는 변수
    pre_gray_frame=None # 이전 프레임을 저장

    # 카운트 다운
    if count_sound:
        count_sound.play()
    for i in range(3, 0, -1):
        start_tick = time.time()
        while time.time() - start_tick < 1:  # 1초 동안 대기하면서 화면 갱신
            _, frame = capture.read()
            if frame is None:
                print("Cannot capture frame")
                break
            frame = cv2.flip(frame, 1)  # 좌우 반전

            # 화면 중앙에 숫자 그리기
            cv2.putText(frame, str(i), (frame_width // 2 - 60, frame_height // 2 + 50),
                        cv2.FONT_HERSHEY_DUPLEX, 5, (0, 255, 255), 15)  #글자 크기 5, 노란색, 두께 15

            cv2.imshow("Coin Game", frame)  # 창의 이름은 같게
            if cv2.waitKey(1) == 27:  # ESC 누르면 종료
                break

    #카운터 다운이 끝난 후 음악 재생
    pygame.mixer.music.play(-1)
    start_time = time.time()  # 게임 시작 시각
    limit_time = 30 # 30초 제한

    while True:
        _, frame = capture.read()
        if frame is None:
            print("Cannot capture frame")
            break
        # 카메라 좌우 반전
        frame=cv2.flip(frame,1)    #위아래는 0
        gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        # 가우시안블러를 이용해서 노이즈 제거(포샵처리)
        gray_frame=cv2.GaussianBlur(gray_frame,(21,21),0)    #홀수로 하는것이 좋다.

        #시간 계산
        elapsed_time = time.time() - start_time
        remaining_time = int(limit_time - elapsed_time)
        # 2. 시간 종료 체크
        if remaining_time <= 0:
            break

        # 첫 프레임이면 현재 프레임을 저장하고 넘어감
        if pre_gray_frame is None:
            pre_gray_frame=gray_frame.copy()
            continue
        # 움직임을 감지 |(현재 프레임 - 이전(과거)프레임)|
        diff_frame=cv2.absdiff(pre_gray_frame,gray_frame)
        # 임계값 조절하기(이진화(흑백으로 보임))
        _, thresh_frame=cv2.threshold(diff_frame,25,255,cv2.THRESH_BINARY)
        # 공과의 충돌 체크
        if coin.is_activate:
            (x1, y1) = (max(0,coin.x-coin.radius), max(0,coin.y-coin.radius))
            (x2, y2) = (min(frame_width,coin.x+coin.radius), min(frame_height,coin.y+coin.radius))

            #사각형 R.O.I 프레임 만들기 / bgr 순
            roi=thresh_frame[y1:y2,x1:x2]
            #지금 R.O.I 영역에 픽셀 카운트
            movement_pixel=cv2.countNonZero(roi)
            area=(x2-x1) * (y2-y1) #사각형의 넓이

            if movement_pixel > area * 0.1: #10% 민감도 / 조정가능
                score+=1
                # 효과음 재생 (비차단 방식)
                if hit_sound:
                    hit_sound.play()

                print(f"터치 성공 - 점수 : {score}")  #콘솔 창에 점수가 나온다.
                #새로운 위치에 공이 나오게 하기
                (coin.x, coin.y) = get_random_position(frame_width, frame_height, coin.radius)

        # 화면에 코인 그리기
        draw_coin(frame,(coin.x, coin.y),coin.radius)

        #화면에 점수 및 시간 표시 / 좌표 설정(왼쪽 상단기준)
        cv2.putText(frame,f"Score : {score}",(5,28),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        cv2.putText(frame, f"Time : {remaining_time}s", (frame_width - 180, 28), 1, 2, (0, 0, 255), 2)
        cv2.imshow("Coin Game",frame)
        #현재프레임을 이전 프레임으로 만들기
        pre_gray_frame=gray_frame.copy()
        if cv2.waitKey(20)==27: # 0.02초 잠깐 기다리고 ESC키 기다리기
            break

    # 게임 종료 화면
    pygame.mixer.music.stop()
    # 마지막 프레임에 결과만 덧칠
    cv2.rectangle(frame, (100, 150), (frame_width - 100, 350), (0, 0, 0), -1)
    cv2.putText(frame, "GAME OVER", (frame_width // 2 - 140, 230), 1, 3, (0, 0, 255), 3)
    cv2.putText(frame, f"Final Score : {score}", (frame_width // 2 - 130, 310), 1, 2, (255, 255, 255), 2)

    cv2.imshow("Coin Game", frame)
    cv2.waitKey(0)  # 아무 키나 누를 때까지 대기

    capture.release()
    cv2.destroyAllWindows()
    return None

if __name__=="__main__":
    main()
