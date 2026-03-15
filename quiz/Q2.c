#define _CRT_SECURE_NO_WARNINGS 
#include <stdio.h>

int main()
{
	//해법 --> 분할&정복
	//1.변수 선언
	int year;
	int currentYear = 2026;
	int age;
	//2.입력
	printf("태어난 년도를 입력하세요 : ");
	scanf_s("%d", &year);
	//3.수식
	age = currentYear - year;
	//4.출력
	printf("만 나이는 %d입니다.",age);

	return 0;
}
