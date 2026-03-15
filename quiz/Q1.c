#define _CRT_SECURE_NO_WARNINGS 
#include <stdio.h>
int main()
{
	//1.변수선언
	int width, height;
	//2.입력
	printf("width 값을 입력하세요 : ");
	scanf("%d", &width);
	printf("height 값을 입력하세요 : ");
	scanf("%d", &height);

	double area = width * height / 2.0; //실수*실수->실수 , 정수/정수=정수 , 정수/실수=실수

	//4.출력
	printf("삼각형 넓이 : %.2lf\n", area);

	return 0;
}
