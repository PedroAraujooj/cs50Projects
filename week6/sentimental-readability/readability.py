# TODO
def main():
    text = input("Text: ")
    nl = count_letters(text)
    nw = count_words(text)
    ns = count_sentences(text)
    l = nl * 100.0 / nw
    s = ns * 100.0 / nw
    index = 0.0588 * l - 0.296 * s - 15.8
    index = round(index)
    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print("Grade " + str(index))


def count_letters(text):
    n = 0
    j = 0
    k = len(text)
    while j < k:
        l = text[j]
        j += 1
        if (l.isalpha()) == True:
            n += 1
    return n


def count_words(text):
    n = 0
    j = 0
    k = len(text)
    while j < k:
        l = ord(text[j])
        j += 1
        if l == 32:
            n += 1
    n += 1
    return n


def count_sentences(text):
    n = 0
    j = 0
    k = len(text)
    while j < k:
        l = ord(text[j])
        j += 1
        if l == 33 or l == 63 or l == 46:
            n += 1

    return n


if __name__ == "__main__":
    main()