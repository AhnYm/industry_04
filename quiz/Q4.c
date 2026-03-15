#define _CRT_SECURE_NO_WARNINGS 
#include <stdio.h>

int main()
{
	int C;
	double F;

	scanf("%d", &C);

	F = ((double)9 / 5) * C + 32; // 정수/정수 -> 정수라 안됨. 정수/실수,실수/실수로

	printf("%.1lf", F);
		
	return 0;
}
