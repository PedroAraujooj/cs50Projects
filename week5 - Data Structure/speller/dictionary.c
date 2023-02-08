// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <cs50.h>
#include <strings.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "dictionary.h"

int nn[1];

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
#define N 26

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int n = hash(word);
    node *c = table[n];
    while (c != NULL)
    {
        if (strcasecmp(c->word, word) == 0)
        {
            return true;
        }
        else
        {
            c = c->next;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int n = word[0];
    if (isupper(word[0]) == 0)
    {
        n -= 97;
    }
    else
    {
        n -= 65;
    }
    return n;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    nn[0] = 0;
    FILE *input = fopen(dictionary, "r");
    if (input == NULL)
    {
        return false;
    }

    char w[LENGTH + 1];
    node *n = NULL;
    while (fscanf(input, "%s", w) != EOF)
    {
        nn[0]++;
        n = malloc(sizeof(node));
        if (n == NULL)
        {
            fclose(input);
            return false;
        }

        strcpy(n->word, w);
        int j = w[0] - 97;
        if (table[j] == NULL)
        {
            n->next = NULL;
            table[j] = n;

        }
        else
        {
            n->next = table[j];
            table[j] = n;
        }


    }

    fclose(input);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    int j = nn[0];
    return j;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {

        while (table[i] != NULL)
        {
            node *tmp = table[i];
            table[i] = table[i]->next;
            free(tmp);
        }

    }
    return true;
}
