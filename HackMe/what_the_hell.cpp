#include<stdio.h>
unsigned long fib[0x98967e];

unsigned int cal_key(unsigned int a, unsigned int b)
{
	unsigned int key, var_c = 1;
	
	while(var_c <= 0x98967e)
	{
		if(var_c > 1)
			fib[var_c] = (fib[var_c - 1] + fib[var_c - 2]) % (1 << 31);
		
		else
			fib[var_c] = var_c;
		
		if(fib[var_c] == a)
			return var_c * b + 1;
		else
			var_c += 1;
	
	}
	return 0;
} 

int main()
{
	unsigned int a, b, key;
	a = 2136772529;
	b = 1234567890;
	key = cal_key(a, b);
	printf("a:%u b:%u key:%u\n", a, b, key);
}

//a:2136772529 b:1234567890 key:4140025247
