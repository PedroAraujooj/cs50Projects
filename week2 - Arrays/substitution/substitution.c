#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

void code(string text, string code);
int main(int argc, string argv[])
{
    string cod = argv[1];
    if (argc < 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    if (argc > 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    if (strlen(argv[1]) > 26 || strlen(argv[1]) < 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    for (int j = 0, k = strlen(argv[1]); j < k; j++)
    {
        char l = (argv[1])[j];
        if (isalpha(l) == false)
        {
            printf("Key must contain 26 characters.\n");
            return 1;
        }
    }
    for (int j = 0, k = strlen(argv[1]); j < k; j++)
    {
        for (int i = 0; i < k; i++)
            if (i != j)
            {
                {
                    if ((argv[1])[j] == (argv[1])[i])
                    {
                        printf("Usage: ./substitution key\n");
                        return 1;
                    }
                }
            }
    }
    string plaintext = get_string("plaintext: ");
    code(plaintext, cod);
    printf("ciphertext: %s\n", plaintext);
    return 0;

}
void code(string text, string code)
{
    for (int j = 0, k = strlen(code); j < k; j++)
    {
        (code)[j] = toupper((code)[j]);
    }
    for (int j = 0, k = strlen(text); j < k; j++)
    {
        char l = text[j];
        if (isalpha(l))
        {
            if (isupper(l))
            {
                l = l - 65;
                text[j] = code[(int)l];
            }
            else
            {
                l = l - 97;
                (text)[j] = code[(int)l];
                text[j] = tolower(text[j]);
            }
        }
    }
}