import cv2
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
import random
def get_random_position(frame_width,frame_height,radius) -> tuple:
    x = random.randint(radius,frame_width - radius) #x축 범위
    y = random.randint(radius, frame_height - radius) #y축 범위
    return (x,y)

def main() -> None:
    capture=cv2.VideoCapture(0) # 지정 카메라 작동
    if not capture.isOpened():
        print("Cannot open camera")
    # 화면의 크기를 가져오기
    frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))  # 캡의 폭을 받아 적용
    frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)) # 캡의 높이을 받아 적용
    print(f"W : {frame_width}, H: {frame_height}")

    # 빨간공의 객체화 및 초기화
    red_ball=Ball() # 생성자 호출 -> 객체화
    red_ball.radius=20  # 20픽셀
    (red_ball.x,red_ball.y)=get_random_position(frame_width,frame_height,red_ball.radius)
    red_ball.is_activate = True

    score=0 # 점수를 저장하는 변수
    pre_gray_frame=None # 이전 프레임을 저장

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

        # 첫 프레임이면 현재 프레임을 저장하고 넘어감
        if pre_gray_frame is None:
            pre_gray_frame=gray_frame.copy()
            continue
        # 움직임을 감지 |(현재 프레임 - 이전(과거)프레임)|
        diff_frame=cv2.absdiff(pre_gray_frame,gray_frame)
        # 임계값 조절하기(이진화(흑백으로 보임))
        _, thresh_frame=cv2.threshold(diff_frame,25,255,cv2.THRESH_BINARY)
        # 공과의 충돌 체크
        if red_ball.is_activate:
            (x1, y1) = (max(0,red_ball.x-red_ball.radius), max(0,red_ball.y-red_ball.radius))
            (x2, y2) = (min(frame_width,red_ball.x+red_ball.radius), min(frame_height,red_ball.y+red_ball.radius))
            #사각형 R.O.I 프레임 만들기 / bgr 순
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
            roi=thresh_frame[y1:y2,x1:x2]

            #지금 R.O.I 영역에 픽셀 카운트
            movement_pixel=cv2.countNonZero(roi)
            area=(x2-x1) * (y2-y1) #사각형의 넓이

            if movement_pixel > area * 0.1: #10% 민감도 / 조정가능
                score+=1
                print(f"터치 성공 - 점수 : {score}")  #콘솔 창에 점수가 나온다.
                #새로운 위치에 공이 나오게 하기
                (red_ball.x, red_ball.y) = get_random_position(frame_width, frame_height, red_ball.radius)

        # 화면에 공 그리기
        cv2.circle(frame,(red_ball.x,red_ball.y),red_ball.radius,(0,0,255),-1)

        #화면에 점수 표시 / 좌표 설정(왼쪽 상단기준)
        cv2.putText(frame,f"score : {score}",(5,28),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        cv2.imshow("HIT_BALL",frame)
        #현재프레임을 이전 프레임으로 만들기
        pre_gray_frame=gray_frame.copy()
        if cv2.waitKey(20)==27: # 0.02초 잠깐 기다리고 ESC키 기다리기
            break
    capture.release()
    cv2.destroyAllWindows()
    return None

if __name__=="__main__":
    main()

