def cleanData(listData):
    for i in range(len(listData)):
        listData[i] = listData[i].strip()
        charList = [char for char in listData[i]]
        listData[i] = charList

    return listData

def printData(listData):
    for row in listData:
        print("".join(row))

def isDataValid(listData):
    if len(listData) == 0:
        return False
    for i in range (len(listData)):
        if len(listData[i]) != len(listData):
            return False
    for i in range(0, len(listData)):
        for j in range(0, len(listData)):
            if listData[i][j] == " ":
                return False
    return True