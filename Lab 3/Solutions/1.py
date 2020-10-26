import sys
import glob

def printFilesInPathWithExtension(path,extension):
    result = glob.glob(path + "\*." + extension)
    for file in result:
        print(file[file.rfind('\\') + 1:len(file)])



if __name__ == "__main__":
    path = sys.argv[1]
    extension = sys.argv[2]
    printFilesInPathWithExtension(path, extension)
 
