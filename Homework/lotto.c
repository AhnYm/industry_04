#1. 리스트 내포 사용
#2. random() 사용 - import random
#3. 중복(x) - .count를 사용해서 1이상이면 리스트에서 포함X
#4. 게임 몇개? (처음에 게임 몇번하고 싶냐고 물어보기) 한번에 5천원(10만원 이하) 20장까지만
#5. 최소 1000번이상 해서 그 중 많이 나온 숫자 고르기 X 6 - 안해도 됨

import random

number = [i for i in range(1,46)]


lotto=[]
max=0
#1000번 랜덤으로 숫자 선택한 것의 중복 된 수를 세서 가장 많이 중복된 값을 넣고 싶은데
# for i in range(6):
    for j in range(1000):
        x=random.choice(number)  #1000번 랜덤으로 숫자 선택
        if lotto.count(x)>max:   #난
            lotto.
