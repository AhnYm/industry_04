#위험 레벨 감지기
from pop import Leds,Sht20,Psd,Cds,Sound,Oled,PiezoBuzzer,delay
import time

#장치 설정
led=Leds()
sht=Sht20()
psd=Psd()
cds=Cds()
sound=Sound()
oled=Oled()
buzzer=PiezoBuzzer()

#oled 초기 설정
oled.init()
oled.setTextSize(s=1)

#각 센서별 기준치 설정
limit_temp=30  #30도 이상이면 위험
limit_humid=60  #40% 이상이면 위험
limit_dist=20  #20cm 이하면 위험
limit_sound=2055  #2055 이상이면 위험
limit_light=600  #600 이하면 위험

#변수 초기화
last_check_time = 0 
danger_count = 0

#각 기준치를 넘을 시에 led등이 켜짐
while True:
    current_time = time.time()
    if current_time - last_check_time >= 5:
        #온도,습도 값
        temp,humid=sht.readTemp(),sht.readHumi()
        #거리 값
        value=psd.readAverage()
        dist=psd.calcDist(value)
        #소리 값
        sound_value=sound.read()
        #조도 값
        light=cds.readAverage()
    
        #위험도 체크
        if temp>=limit_temp:
            danger_count+=1 
        if humid>=limit_humid:
            danger_count+=1  
        if dist<=limit_dist:
            danger_count+=1  
        if sound_value>=limit_sound:
            danger_count+=1  
        if light<=limit_light:
            danger_count+=1  
        
        #oled상 값들
        oled.clearDisplay()
        oled.setCursor(0,2)
        oled.print(f"<HAZARD LEVEL> - {danger_count}")
        oled.setCursor(0,8)
        oled.print("-"*21)
        oled.setCursor(0,15)
        oled.print(f"Temperation : {temp:.2f}C")
        oled.setCursor(0,25)
        oled.print(f"Humidity : {humid:.2f}%")
        #거리 값
        oled.setCursor(0,35)
        oled.print(f"Distance : {dist:.2f}cm")
        #소리 값
        oled.setCursor(0,45)
        oled.print(f"Sound : {sound_value:.2f}")
        # 조도 값
        oled.setCursor(0,55)
        oled.print(f"Light : {light:.2f}")
        oled.display()
                
        last_check_time = current_time # 마지막 체크 시점 갱신
        
    #단계별 led와 부저 제어
    # 레벨 5(위험 단계): 가장 길게 연속음
    if danger_count == 5:
        led.allOn()
        buzzer.tone(4, 2, 1)
        delay(10)
        led.allOff()
    # 레벨 3~4(경계 단계): 빠르게
    elif danger_count>= 3:
        for i in range(danger_count): 
            led[i].on()
        buzzer.tone(4, 2, 8)
        delay(100)
        led.allOff()
        delay(100)
    # 레벨 1~2(주의 단계): 느리게
    elif danger_count>= 1:
        for i in range(danger_count): 
            led[i].on()
        buzzer.tone(4, 2, 8)
        delay(200)
        led.allOff()
        delay(200)  
    else:
        # 레벨 0(안전 상태) : 무반
        led.allOff()
        delay(50)
