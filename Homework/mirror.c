#10x10의 list
#상하좌우 뒤집기/좌로,우로 회전/원점 대칭
#검정만 255,나머지는 0
L_pixel=[[0,0,0,0,0,0,0,0,0,0],
         [0,255,255,0,0,0,0,0,0,0],
         [0,255,255,0,0,0,0,0,0,0],
         [0,255,255,0,0,0,0,0,0,0],
         [0,255,255,0,0,0,0,0,0,0],
         [0,255,255,0,0,0,0,0,0,0],
         [0,255,255,0,0,0,0,0,0,0],
         [0,255,255,255,255,255,255,255,0,0],
         [0,255,255,255,255,255,255,255,0,0],
         [0,0,0,0,0,0,0,0,0,0]
         ]

#좌우 반전
for i in L_pixel:
    L_pixel_reverse=reversed(i)
    print(list(L_pixel_reverse))
print()

#상하 반전
a=list(reversed(L_pixel))
for i in a:
    print(i,end="\n")
print()

#원점 대칭
for i in a:
    L_pixel_one_reverse = reversed(i)
    print(list(L_pixel_one_reverse))
