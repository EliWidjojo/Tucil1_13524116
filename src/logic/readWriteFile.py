import os

def readFile(fileName):
    if os.path.exists(fileName):
        with open(fileName, "r") as f:
            return f.readlines()

    print("File tidak ada!")
    return

def writeFile(fileName, listData):
    f = open(fileName, "w") 

    for row in listData:
        f.write("".join(row) + "\n")

    f.close()


