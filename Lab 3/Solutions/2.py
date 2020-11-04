import sys
import os
nextStr = "├───"
endStr  = "└───"
spaceStr= "   "

def getOnlyFolders(path):
    return [i for i in os.listdir(path) if os.path.isdir(path + "\\" + i)]

def printTree(strStart,path, mod=0):
    folders = getOnlyFolders(path)
    for i in range(len(folders)):

        str = strStart + spaceStr

        if(mod==1):
            str = ""

        startStr = "│"

        if (i == len(folders) - 1):
            str += endStr
            startStr = " "
        else:
            str += nextStr

        print(str + folders[i])

        if(mod==1):
            printTree(startStr+spaceStr, path + "\\" + folders[i])
        else:
            printTree(strStart + spaceStr + startStr, path + "\\" + folders[i])

if __name__ == "__main__":
    path = sys.argv[1]
    if (path.rfind('\\') == -1):
        print(path)
    else:
        print(path[path.rfind('\\') + 1:len(path)])

    printTree("",path,1) 
