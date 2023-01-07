#include <cs50.h>
#include <stdio.h>                      //sorry, the code got too big and I couldn't style it
bool checksum(long num);

void CreditCard(long num);

int main(void)
{
long num = get_long("Number: ");
   if(checksum(num))
   {
    CreditCard(num);
   }
   else printf("INVALID\n");
}

bool checksum(long num)
{
    int result1=0;
	int result2=0;
	int k=0;                            //I used this "k" to differentiate each numer and where to save them
	long i;                             // I made this "i" outside the "for" because I used it in the lines 60 and 68
	for( i=10; i<=num; i*=10)
    {
	    long j= num%i;
		num-=j;
		k++;
		while(j>=10)
        {
			j/=10;
		}
		j=(int)j;
		if(k % 2!=0)
        {
		    result1+=j;
		}
		if(k % 2==0)
        {
			if(j*2>=10)
            {
			    int l= (int)(j*2)%10;
				j= (int)(j*2)/10;
				result2+= l;
				result2+= j;
			}
			else
            {
			    result2+=j*2;
			}
		}
	}
	k++;
	if(k%2!=0)
    {
	    result1+=num/(i/10);
	}
	if(k%2==0)
    {
        int a;
	    a=(int)(num/(i/10))*2;
		if(a>9)
		{
		    int l= a%10;
		    a = (a)/10;
			result2+= l;
			result2+= a;
        }
        else result2+=(num/(i/10))*2;
    }
    if((result1 + result2)%10==0)
    {
        return true;
    }
    else
    {
        return false;
    }
}

void CreditCard(long num)
{
	if((num>=1000000000000000 && num<=9999999999999999)&&((num/100000000000000)>50 && (num/100000000000000)<56))
		{
			printf("MASTERCARD\n");
		}
		else if((num>=100000000000000 && num<=999999999999999)&&((num/10000000000000)==37 || (num/10000000000000)==34))
		{
			printf("AMEX\n");
		}
		else if(num>=1000000000000 && num<=9999999999999999)
		{
			for(long i=1000000000000; i<=num; i*=10)
			{
				int k =(int)(num/i);
				if(k<10)
				{
					if(k==4)
					{
						printf("VISA\n");
					}
					else
					{
						printf("INVALID\n");
					}
				}

			}
		}
        else printf("INVALID\n");
}