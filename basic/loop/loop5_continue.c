#define _CRT_SECURE_NO_WARNINGS 
#include <stdio.h>

int main()
{
	for (int i = 1; i <= 100; i++)
	{
		if (i%3 == 0 || i%5==0)
		{
			continue;
		}
		printf("%d\n", i);
	}
		
	return 0
}
