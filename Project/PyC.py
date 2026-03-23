#식물 키우기 / 위험 레벨 감지기
from pop import Leds,Sht20,Cds,Sound,Psd,Oled,PiezoBuzzer,delay
led = Leds()
sht=Sht20()
cds=Cds()
sound=Sound()
psd=Psd()
oled=Oled()

#oled 초기 설정
oled.init()
oled.setTextSize(s=1)
oled.clearDisplay()

#각 기준치를 넘을 시에 led등이 증가/ 3개이상은 부저가 울리게
while True:
    #온도와 습도 측정
    temp,humid=sht.readTemp(),sht.readHumi()
    #소리 측정
    sound_value=sound.readAverage()
    #거리 측정
    value = psd.readAverage()
    distance=psd.calcDist(value)
    #빛 측정
    light=cds.readAverage()
    #oled상 값들
    oled.clearDisplay()
    oled.setCursor(5,5)
    oled.print(f"Temperation : {temp:.2f}C")
    oled.setCursor(5,15)
    oled.print(f"Humidity : {humid:.2f}%")
    #소리 값
    oled.setCursor(5,25)
    oled.print(f"Sound : {sound_value:.2f}")
    #거리 값
    oled.setCursor(5,35)
    oled.print(f"Distance : {distance:.2f}cm")
    # 빛의 값
    oled.setCursor(5,45)
    oled.print(f"Light : {light:.2f}")
    oled.display()
    delay(1000)
    
    
