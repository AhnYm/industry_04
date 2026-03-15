#define _CRT_SECURE_NO_WARNINGS 
#include <stdio.h>

int main()
{
	int age;
	printf("나이를 입력하세요 : ");
	scanf("%d", &age);

	if (age >= 65) {
		printf("무료\n");
	}
	else if (age >= 13) {
		printf("10000원\n");
	}
	else {
		printf("5000원\n");
	}
	printf("단, 나이는 0세이상 100세이하 값만 입력됩니다.");

	return 0;
}
