import argparse

def FindCenterOfRectangle(startX, endX, startY, endY):
        return ((startX + endX) // 2, (startY + endY) // 2)

def placeTromino(x1, y1, x2, y2, x3, y3, n):
    global Map
    Map[x1][y1] = n
    Map[x2][y2] = n
    Map[x3][y3] = n
    
def printOutput(Map):
    size = len(Map)
    print()
    for i in range(size):
        for j in range(size):
            print("%s" % Map[i][j], end=" ")
        print()
    print()
    
def outputToFile(Map):
    size = len(Map)
    filename= 'output.txt'
    with open(filename, 'w') as f:
        for i in range(size):
            for j in range(size):
                f.write("%s " % Map[i][j])
            f.write("\n")
        f.write("\n")

def SolveTromino(n, startX, endX, startY, endY, openX, openY):
        global Map
        cX, cY = FindCenterOfRectangle(startX, endX, startY, endY)

        firstX, firstY = cX, cY
        secondX, secondY = cX+1, cY
        thirdX, thirdY = cX, cY+1
        fourthX, fourthY = cX+1, cY+1

        if n!=1:
            color1='G'
            color2='G'
        else:
            color1='B'
            color2='R'
        
        if openX <= cX:
            if openY <= cY:
                placeTromino( cX, cY+1, cX+1, cY+1, cX+1, cY, color1)
                firstX, firstY = openX, openY
            else:
                placeTromino( cX, cY, cX+1, cY, cX+1, cY+1, color2)
                secondX, secondY = openX, openY
        else:
            if openY <= cY:
                placeTromino( cX, cY, cX, cY+1, cX+1, cY+1, color2)
                thirdX, thirdY = openX, openY
            else:
                placeTromino( cX, cY, cX+1, cY, cX, cY+1, color1)
                fourthX, fourthY = openX, openY

        if n==1:
            return
        else:
            SolveTromino(n-1, startX, cX, startY, cY, firstX, firstY)
            SolveTromino(n-1, startX, cX, cY, endY, secondX, secondY)
            SolveTromino(n-1, cX, endX, startY, cY, thirdX, thirdY)
            SolveTromino(n-1, cX, endX, cY, endY, fourthX, fourthY)

def main():
    parser = argparse.ArgumentParser(description='Tromino Puzzle SolveTrominor')
    parser.add_argument('n', type=int, help='Rectangle size (size will be 2^n x 2^n)')
    args = parser.parse_args()
    
    global Map
    n = args.n
    if n==1:
        openX = 0
        openY = 1
    elif n>1:
        openX = 3
        openY = 3
    else:
        raise ValueError("Invalid value of rectangle size")
        
    size = 2**n
    Map = [['X' if i==openX and j==openY else '0' for j in range(size)] for i in range(size)]
    printOutput(Map)
    SolveTromino(n, 0, size-1, 0, size-1, openX, openY)
    printOutput(Map)
    outputToFile(Map)


if __name__ == "__main__":
    main()