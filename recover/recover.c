#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    typedef uint8_t BYTE;
    if (argc != 2)
    {
        printf("you must './recover INPUT.raw'\n");
        return 1;
    }
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }
    int n = 0;
    BYTE *buff = malloc(sizeof(BYTE) * 512); //buff used to read card.raw
    if (buff == NULL)                        //checking if there is space to store the buff
    {
        return 1;
    }
    char *filename = malloc(sizeof(char) * 8); //buffer for sprintf
    if (filename == NULL)                      //checking space
    {
        return 1;
    }
    FILE *img = NULL;                           // pointer to new images, will be started only when it find JPGs
    sprintf(filename, "%03i.jpg", n);
    while (fread(buff, sizeof(BYTE), 512, input) == 512)
    {
        if (buff[0] == 0xff && buff[1] == 0xd8 && buff[2] == 0xff && (buff[3] & 0xf0) == 0xe0)
        {
            if (n == 0)
            {
                img = fopen(filename, "w");
                fwrite(buff, sizeof(BYTE), 512, img);
                n++;
            }
            else
            {
                fclose(img);
                sprintf(filename, "%03i.jpg", n);
                img = fopen(filename, "w");
                fwrite(buff, sizeof(BYTE), 512, img);
                n++;
            }
        }
        else
        {
            if (img != NULL)
            {
                fwrite(buff, sizeof(BYTE), 512, img);
            }
        }
    }
    //closing all spaces to avoid memory mistakes
    fclose(img);
    fclose(input);
    free(filename);
    free(buff);

}