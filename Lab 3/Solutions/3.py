import sys
import glob


if __name__ == "__main__":
    listNumbers = list(sys.argv)
    listNumbers.reverse()
    listNumbers.pop()
    listNumbers.sort()
    print(listNumbers)
