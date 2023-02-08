#include "helpers.h"
#include <math.h>
void blurNew(double *n, double *B, double *R, double *G, int height, int width, RGBTRIPLE image[height][width], int i, int j);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            double b = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0;
            int x = round(b);
            image[i][j].rgbtRed = x;
            image[i][j].rgbtBlue = x;
            image[i][j].rgbtGreen = x;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
            RGBTRIPLE aux = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = aux;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE arr[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            double R = image[i][j].rgbtRed;
            double G = image[i][j].rgbtGreen;
            double B = image[i][j].rgbtBlue;
            double n = 1.0;
            if (i - 1 >= 0 && i - 1 < height && j - 1 >=0  && j - 1 < width)
            {
                blurNew(&n, &B, &R, &G, height, width, image, i-1, j-1);
            }
            if(i-1 >= 0 && i-1 < height && j>=0 && j < width)
            {
                blurNew(&n, &B, &R, &G, height, width, image, i-1, j);
            }
            if(i-1 >= 0 && i-1 < height && j+1>=0 && j+1 < width)
            {
                blurNew(&n, &B, &R, &G, height, width, image, i-1, j+1);
            }
            if(i >= 0 && i < height && j-1>=0 && j-1 < width)
            {
                blurNew(&n, &B, &R, &G, height, width, image, i, j-1);
            }
            if(i >= 0 && i < height && j+1>=0 && j+1 < width)
            {
                blurNew(&n, &B, &R, &G, height, width, image, i, j+1);
            }
            if(i+1 >= 0 && i+1 < height && j-1>=0 && j-1 < width)
            {
                blurNew(&n, &B, &R, &G, height, width, image, i+1, j-1);
            }
            if(i+1 >= 0 && i+1 < height && j>=0 && j < width)
            {
                blurNew(&n, &B, &R, &G, height, width, image, i+1, j);
            }
            if(i+1 >= 0 && i+1 < height && j+1>=0 && j+1 < width)
            {
                blurNew(&n, &B, &R, &G, height, width, image, i+1, j+1);
            }
            arr[i][j].rgbtBlue = round(B / n);
            arr[i][j].rgbtRed = round(R / n);
            arr[i][j].rgbtGreen = round(G / n);
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width); j++)
        {
            image[i][j].rgbtBlue = arr[i][j].rgbtBlue;
            image[i][j].rgbtRed = arr[i][j].rgbtRed;
            image[i][j].rgbtGreen = arr[i][j].rgbtGreen;
        }
    }

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE arr[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j< width; j++)
        {
            double RGx = 0;
            double GGx = 0;
            double BGx = 0;
            double RGy = 0;
            double GGy = 0;
            double BGy = 0;
            //int n= 1;
            if(i-1 >= 0 && i-1 < height && j-1>=0 && j-1 < width)
            {
                BGx+=image[i-1][j-1].rgbtBlue*-1;
                RGx+=image[i-1][j-1].rgbtRed*-1;
                GGx+=image[i-1][j-1].rgbtGreen*-1;
                BGy+=image[i-1][j-1].rgbtBlue*-1;
                RGy+=image[i-1][j-1].rgbtRed*-1;
                GGy+=image[i-1][j-1].rgbtGreen*-1;
            }

            if(i-1 >= 0 && i-1 < height && j>=0 && j < width)
            {
                BGx+=image[i-1][j].rgbtBlue*0;
                RGx+=image[i-1][j].rgbtRed*0;
                GGx+=image[i-1][j].rgbtGreen*0;
                BGy+=image[i-1][j].rgbtBlue*-2;
                RGy+=image[i-1][j].rgbtRed*-2;
                GGy+=image[i-1][j].rgbtGreen*-2;
            }

            if(i-1 >= 0 && i-1 < height && j+1>=0 && j+1 < width)
            {
                BGx+=image[i-1][j+1].rgbtBlue*1;
                RGx+=image[i-1][j+1].rgbtRed*1;
                GGx+=image[i-1][j+1].rgbtGreen*1;
                BGy+=image[i-1][j+1].rgbtBlue*-1;
                RGy+=image[i-1][j+1].rgbtRed*-1;
                GGy+=image[i-1][j+1].rgbtGreen*-1;
            }

            if(i >= 0 && i < height && j-1>=0 && j-1 < width)
            {
                BGx+=image[i][j-1].rgbtBlue*-2;
                RGx+=image[i][j-1].rgbtRed*-2;
                GGx+=image[i][j-1].rgbtGreen*-2;
                BGy+=image[i][j-1].rgbtBlue*0;
                RGy+=image[i][j-1].rgbtRed*0;
                GGy+=image[i][j-1].rgbtGreen*0;
            }

            if(i >= 0 && i < height && j+1>=0 && j+1 < width)
            {
                BGx+=image[i][j+1].rgbtBlue*2;
                RGx+=image[i][j+1].rgbtRed*2;
                GGx+=image[i][j+1].rgbtGreen*2;
                BGy+=image[i][j+1].rgbtBlue*0;
                RGy+=image[i][j+1].rgbtRed*0;
                GGy+=image[i][j+1].rgbtGreen*0;
            }

            if(i+1 >= 0 && i+1 < height && j-1>=0 && j-1 < width)
            {
                BGx+=image[i+1][j-1].rgbtBlue*-1;
                RGx+=image[i+1][j-1].rgbtRed*-1;
                GGx+=image[i+1][j-1].rgbtGreen*-1;
                BGy+=image[i+1][j-1].rgbtBlue*1;
                RGy+=image[i+1][j-1].rgbtRed*1;
                GGy+=image[i+1][j-1].rgbtGreen*1;
            }

            if(i+1 >= 0 && i+1 < height && j>=0 && j < width)
            {
                BGx+=image[i+1][j].rgbtBlue*0;
                RGx+=image[i+1][j].rgbtRed*0;
                GGx+=image[i+1][j].rgbtGreen*0;
                BGy+=image[i+1][j].rgbtBlue*2;
                RGy+=image[i+1][j].rgbtRed*2;
                GGy+=image[i+1][j].rgbtGreen*2;
            }

            if(i+1 >= 0 && i+1 < height && j+1>=0 && j+1 < width)
            {
                BGx+=image[i+1][j+1].rgbtBlue*1;
                RGx+=image[i+1][j+1].rgbtRed*1;
                GGx+=image[i+1][j+1].rgbtGreen*1;
                BGy+=image[i+1][j+1].rgbtBlue*1;
                RGy+=image[i+1][j+1].rgbtRed*1;
                GGy+=image[i+1][j+1].rgbtGreen*1;
            }

            double Rg = sqrt((RGx * RGx)+(RGy * RGy));
            double Gg =  sqrt((GGx * GGx)+(GGy * GGy));
            double Bg =  sqrt((BGx * BGx)+(BGy * BGy));
            Rg = round(Rg);
            Gg = round(Gg);
            Bg = round(Bg);
            if (Rg > 255)
            {
                Rg = 255;
            }
            if (Gg > 255)
            {
                Gg = 255;
            }
            if (Bg > 255)
            {
                Bg = 255;
            }
            arr[i][j].rgbtRed = (int)Rg;
            arr[i][j].rgbtGreen = (int)Gg;
            arr[i][j].rgbtBlue = (int)Bg;

        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width); j++)
        {
            image[i][j].rgbtBlue = arr[i][j].rgbtBlue;
            image[i][j].rgbtRed = arr[i][j].rgbtRed;
            image[i][j].rgbtGreen = arr[i][j].rgbtGreen;
        }
    }
    return;
}

void blurNew(double *n, double *B, double *R, double *G, int height, int width, RGBTRIPLE image[height][width], int i, int j)
{
    *B+=image[i][j].rgbtBlue;
    *R+=image[i][j].rgbtRed;
    *G+=image[i][j].rgbtGreen;
    *n+=1;
}