import string
import itertools

def createWordList(iters):
    """
    :param `chrs` is characters to iterate.
    :param `min_length` is minimum length of characters.
    :param `max_length` is maximum length of characters.
    :param `output` is output of wordlist file.
    """
    chrs = string.printable.replace(' \t\n\r\x0b\x0c', '')

    wordlist = []
    for n in range(iters, iters + 1):
        for xs in itertools.product(chrs, repeat=n):
            chars = ''.join(xs)
            wordlist.append(chars)
    return wordlist
