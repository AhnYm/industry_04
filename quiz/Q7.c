#define _CRT_SECURE_NO_WARNINGS 
#include <stdio.h>

int main()
{
	//1.변수선언
	int kor, eng, mat;
	int tot;
	double avg;

	printf("국어,영어,수학 순으로 성적을 입력하세요. ");
	scanf("%d %d %d", &kor, &eng, &mat);
	//2.수식
	tot = kor + eng + mat;
	avg = (double)tot / 3;  // <==> tot/3.0;
	//3.출력
	printf("총점 : %d\n", tot);
	printf("평균 : %.2lf\n", avg);

	return 0;
}
