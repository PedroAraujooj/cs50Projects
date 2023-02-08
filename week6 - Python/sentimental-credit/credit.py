# TODO

def checksum(num):
    result1 = 0
    result2 = 0
    k = 0
    i = 10
    while i <= num:
        j = num % i
        num = num - j
        k += 1
        while j >= 10:
            j = j/10
        j = int(j)
        if k % 2 != 0:
            result1 += j
        if k % 2 == 0:
            if j*2 >= 10:
                l = int((j*2) % 10)
                j = int((j*2) / 10)
                result2 += l
                result2 += j
            else:
                result2 += j*2
        i = i*10
    k += 1
    if k % 2 != 0:
        result1 += num/(i/10)
    if k % 2 == 0:
        a = int((num/(i/10))*2)
        if a > 9:
            l = a % 10
            a = (a)/10
            result2 += l
            result2 += a
        else:
            result2 += (num/(i/10))*2

    if (result1 + result2) % 10 == 0:
        return True
    else:
        return False


def CreditCard(num):
    if (num >= 1000000000000000 and num <= 9999999999999999) and ((num/100000000000000) > 50 and (num/100000000000000) < 56):
        print("MASTERCARD")
    elif (num >= 100000000000000 and num <= 999999999999999) and (int((num/10000000000000)) == 37 or (int(num/10000000000000)) == 34):
        print("AMEX")
    elif (num >= 1000000000000 and num <= 9999999999999999):
        i = 1000000000000
        while i <= num:
            k = (int)(num/i)
            i = i*10
            if k < 10:
                if k == 4:
                    print("VISA")
                else:
                    print("INVALID")

    else:
        print("INVALID")


def main():
    num = int(input("Number: "))
    if checksum(num) == True:
        CreditCard(num)
    else:
        print("INVALID")


if __name__ == "__main__":
    main()