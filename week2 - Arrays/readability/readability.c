#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <math.h>
#include <string.h>
int count_sentences(string text);
int count_words(string text);
int count_letters(string text);
int main(int argc, string argv[])
{
    int nl; // numero de letras
    int nw;
    int ns;
    float index;
    string text = get_string("Text: ");
    nl = count_letters(text);
    nw = count_words(text);
    ns = count_sentences(text);
    float l = nl * 100.0 / nw;
    float s = ns * 100.0 / nw;
    index = 0.0588 * l - 0.296 * s - 15.8;
    index = round(index);
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %.0f\n", index);
    }

    //printf("%i\n", nw);
    //printf("%i\n", nl);
    //printf("%i\n", ns);
}
int count_letters(string text)
{
    int n = 0;
    for (int j = 0, k = strlen(text); j < k; j++)
    {
        char l = text[j];
        if (isalpha(l))
        {
            n++;
        }
    }
    return n;
}
int count_words(string text)
{
    int n = 0;
    for (int j = 0, k = strlen(text); j < k; j++)
    {
        char l = text[j];
        if (l == 32)
        {
            n++;
        }
    }
    n++;
    return n;
}
int count_sentences(string text)
{
    int n = 0;
    for (int j = 0, k = strlen(text); j < k; j++)
    {
        char l = text[j];
        if (l == 33 || l == 63 || l == 46)
        {
            n++;
        }
    }
    return n;
}