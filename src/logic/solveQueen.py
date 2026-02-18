def permutations(arr, r):
    arr = list(arr)
    if r == 0:
        yield []
    else:
        for i in range(len(arr)):
            rest = arr[:i] + arr[i+1:]
            for p in permutations(rest, r-1):
                yield [arr[i]] + p

# Hitung jumlah Queens
def numberOfColors(listData):
    l1 = []
    count = 0
    for i in range (len(listData)):
        for char in listData[i]:
            if char not in l1:
                count +=1 
                l1.append(char)
    return count

# Generate Position
def generateSquarePosition(count):
    l = []
    a = 0
    for i in range (count):
        for j in range (count):
            l.append(a)
            a += 1

    return l 


def valid_warna(square, ori):
    warnaTerpakai = set()
    n = len(square)

    for i in range(n):
        for j in range(n):
            if square[i][j] == '#':
                warna = ori[i][j]
                if warna in warnaTerpakai:
                    return False
                warnaTerpakai.add(warna)

    return True

def pemeriksaan(listData): 
    #pemeriksaan horizontal    
    for i in range (len(listData)): 
        horizontalTag = False
        for j in range (len(listData[i])): 
            if (listData[i][j] == '#') and (horizontalTag != True):
                horizontalTag = True
            elif (listData[i][j] == '#') and (horizontalTag == True):
                return False
            
            if (listData [i][j] == '#'):
                if (i-1 >= 0 and j-1>=0):
                    if listData[i-1][j-1] == '#':
                        return False
                
                if (i-1 >= 0 and j+1 < len(listData)):
                    if (listData[i-1][j+1] == '#'):
                        return False

                if (i+1 < len(listData) and j-1 >= 0):
                    if (listData[i+1][j-1] == '#'):
                        return False

                if (i+1 < len(listData) and j+1 < len(listData)):
                    if (listData[i+1][j+1] == '#'):
                        return False
    
    #pemeriksaan vertikal
    for j in range (len(listData)): 
        verticalTag = False
        for i in range (len(listData[i])):            
            if (listData[i][j] == '#') and (verticalTag != True):
                verticalTag = True
            elif (listData[i][j] == '#') and (verticalTag == True):
                return False
            
    return True

def solveMurni(listData, visualCallback=None):
    jumQueen = numberOfColors(listData)
    lPosition = generateSquarePosition(len(listData))
    iteration = 0
    for p in permutations(lPosition, jumQueen):
        iteration += 1
        square = [list(row) for row in listData]

        for i in range(len(p)):
            row = p[i]//len(listData)
            column = p[i] % len(listData)
            square[row][column] = '#'
        if visualCallback and iteration % 100 == 0:
            visualCallback(square)

        if pemeriksaan(square) and valid_warna(square, listData):
            return square, iteration

    return None, iteration


def solve(listData, visualCallback=None):
    iteration = 0
    n = len(listData)
    r = numberOfColors(listData)
    for cols in permutations(range(n), r):
        iteration += 1
        square = [list(row) for row in listData]

        for row in range(r):
            square[row][cols[row]] = '#'
        if visualCallback and iteration % 100 == 0:
            visualCallback(square)
        if pemeriksaan(square) and valid_warna(square, listData):
            return square, iteration
    return None, iteration




        






