import random

def getOptionString(optionValue):
    return ['papier', 'kamień', 'nożyce'][optionValue - 1]

def printResult(results):
    print('-'*40)
    resultStr = "Zwycięzca:\t\t\t"
    if (results[0] > results[1]):
        resultStr += "Gracz"
    elif (results[0] < results[1]):
        resultStr += "Komputer"
    else:
        resultStr += "Gracz\t|\tKomputer"

    resultStr += "\nLiczba zwycięstw:\t\t"
    if (results[0] > results[1]):
        resultStr += str(results[0])
    elif (results[0] < results[1]):
        resultStr += str(results[1])
    else:
        resultStr +=  str(results[0]) + "\t|\t" + str(results[1])

    resultStr += "\nLiczba porażek:\t\t\t"
    if (results[0] > results[1]):
        resultStr += str(results[1])
    elif (results[0] < results[1]):
        resultStr += str(results[0])
    else:
        resultStr += str(results[1]) + "\t|\t" + str(results[0])

    resultStr += "\nLiczba remisów:\t\t\t"
    if (results[0] == results[1]):
        resultStr += str(results[2]) + "\t|\t" + str(results[2])
    else:
        resultStr += str(results[2])

    print(resultStr)

def startGame(roundsNum):

    results=[0,0,0]
    currentRoundNum = 0

    while currentRoundNum < roundsNum:

        currentRoundNum+=1
        playerOption = -1

        isGoodInput = False

        while not isGoodInput:
            isGoodInput = True
            try:
                playerOption = int(input("Podaj liczbę 1-3, gdzie 1 - papier, 2 - kamień, 3 - nożyce: "))
                if (playerOption<1 or playerOption>3):
                    isGoodInput = False
            except ValueError:
                isGoodInput = False

        computerOption = random.randint(1, 3)

        printString="Gracz - "+getOptionString(playerOption)+" , Komputer - "+getOptionString(computerOption)
        print(printString)

        resultStr="Wynik: "

        if(playerOption==computerOption):
            results[2]=results[2]+1
            resultStr="Remis"
        elif((playerOption==1 and computerOption==2) or (playerOption==2 and computerOption==3) or (playerOption==3 and computerOption==1)):
            results[0]+=1
            resultStr = "Gracz wygrywa"
        else:
            results[1]+=1
            resultStr = "Gracz przegrywa"
        print(resultStr)

    printResult(results)


if __name__ == "__main__":
    print("Gra \"papier kamień nożyce\" ")
    roundsNum = int(input("Podaj liczbę rund: "))
    startGame(roundsNum) 
