import argparse

def FindCenter(startX, endX, startY, endY):
        return ((startX + endX) // 2, (startY + endY) // 2)

def placeTromino(x1, y1, x2, y2, x3, y3, n):
    global tileMap
    tileMap[x1][y1] = n
    tileMap[x2][y2] = n
    tileMap[x3][y3] = n
    
def printMap(tileMap):
    size = len(tileMap)
    print()
    for i in range(size):
        for j in range(size):
            print("%s" % tileMap[i][j], end=" ")
        print()
    print()

def solve(n, startX, endX, startY, endY, tileX, tileY):
        global tileMap
        cX, cY = FindCenter(startX, endX, startY, endY)

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
        
        if tileX <= cX:
            if tileY <= cY:
                placeTromino( cX, cY+1, cX+1, cY+1, cX+1, cY, color1)
                firstX, firstY = tileX, tileY
            else:
                placeTromino( cX, cY, cX+1, cY, cX+1, cY+1, color2)
                secondX, secondY = tileX, tileY
        else:
            if tileY <= cY:
                placeTromino( cX, cY, cX, cY+1, cX+1, cY+1, color2)
                thirdX, thirdY = tileX, tileY
            else:
                placeTromino( cX, cY, cX+1, cY, cX, cY+1, color1)
                fourthX, fourthY = tileX, tileY

        if n==1:
            return
        else:
            solve(n-1, startX, cX, startY, cY, firstX, firstY)
            solve(n-1, startX, cX, cY, endY, secondX, secondY)
            solve(n-1, cX, endX, startY, cY, thirdX, thirdY)
            solve(n-1, cX, endX, cY, endY, fourthX, fourthY)

def main():
    parser = argparse.ArgumentParser(description='Tromino Puzzle Solver')
    parser.add_argument('n', type=int, help='Rectangle size (size will be 2^n x 2^n)')
    args = parser.parse_args()
    
    global tileMap
    n = args.n
    if n==1:
        tileX = 0
        tileY = 1
    elif n>1:
        tileX = 3
        tileY = 3
    else:
        raise ValueError("Invalid value of rectangle size")
        
    size = 2**n
    tileMap = [['x' if i==tileX and j==tileY else '0' for j in range(size)] for i in range(size)]
    printMap(tileMap)
    solve(n, 0, size-1, 0, size-1, tileX, tileY)
    printMap(tileMap)


if __name__ == "__main__":
    main()