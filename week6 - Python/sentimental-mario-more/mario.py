# TODO
from cs50 import get_int


def main():
    while True:
        try:
            high = int(input("Height: "))
            if high <= 8 and high >= 1:
                break
        except ValueError:
            print("That's not an integer!")
    height(high + 1)


def height(high):
    for x in range(1, high, 1):
        for y in range(0, high - 1 - x, 1):
            print(" ", end="")
        for y in range(0, x, 1):
            print("#", end="")
        print("  ", end="")
        for y in range(0, x, 1):
            print("#", end="")
        print("")


if __name__ == "__main__":
    main()