#1. 리스트 내포 사용
#2. random() 사용 - import random
#3. 중복(x) - .count를 사용해서 1이상이면 리스트에서 포함X
#4. 게임 몇개? (처음에 게임 몇번하고 싶냐고 물어보기) 한번에 5천원(10만원 이하) 20장까지만
#5. 최소 1000번이상 해서 그 중 많이 나온 숫자 고르기 X 6
import random

print("="*40)
print("               로또 생성기              ")
print("="*40)
# 게임 시작
while True:
    buy_lotto_number = int(input("구매할 로또 수를 입력하세요 (1장에 5,000원 / 최대 20장): "))
    if buy_lotto_number > 20:
        print("최대 20장까지(10만 원)입니다. 다시 입력해주세요.")
    elif buy_lotto_number == 0:
        print("1장 이상 구매해야 합니다. 다시 입력해주세요.")
    else:
        break
#로또의 1~46개의 숫자를 저장
number = [i for i in range(1,46)]

for i in range(1, buy_lotto_number + 1):
    print(f"\n[{i}번째 장]")
    lotto_cnt = 0
    #1000번 랜덤으로 숫자 선택한 것의 중복 된 수를 세서 가장 많이 중복된 값을 넣기
    print('-'*40)
    while lotto_cnt<5:
        lotto_cnt += 1
        lotto = []
        while len(lotto)<6:
            result = []
            dictionary = {}
            for i in range(1000):
                x=random.choice(number)  #1000번 랜덤으로 숫자 선택
                result.append(x)
            #딕셔너리와 .count를 사용해서 가장 많이 중복된 값 확인
            for key in result:
                dictionary[key]=result.count(key)
            max_number = max(dictionary, key=dictionary.get)
            # 중복시 제거
            if max_number not in lotto:
                lotto.append(max_number)
            #정렬 맞추기
        lotto.sort()
        print(f"{lotto_cnt}번째 로또 번호 : {lotto}")
    print('-' * 40)
    print('금액 : %33s'%('5000원'))
