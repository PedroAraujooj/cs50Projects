#include <cs50.h>
#include <stdio.h>
void height(int);

int main(void)
{
    int high;
    do
    {
        high = get_int("Height: ");
    }
    while (high > 8 || high < 1);

    height(high);

}

void height(int high)
{
    for (int i = 1; i <= high; i++)             //this "for" is about each line of the pyramid
    {
        for (int j = 1; j <= high - i; j++)     //this "for" is about each space before the hashes
        {
            printf(" ");
        }
        for (int j = 1; j <= i; j++)            //this "for" is about each hash before the mid gap
        {
            printf("#");
        }
        printf("  ");                           //this is the mid gap
        for (int j = 1; j <= i; j++)            //this "for" is about each hash after the mid gap
        {
            printf("#");
        }
        printf("\n");                           // this command is to change the line
    }
}