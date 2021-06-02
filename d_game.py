import pygame, sys
from pygame.locals import*

DIMENSION = 7
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOARDRADIUS = 230
BOARDCENTRE = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2))
MARBLERADIUS = 20
GAP = int((2*BOARDRADIUS - 7*2*MARBLERADIUS)/8)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARKRED = (200, 0, 0)
GREEN = (0, 100, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

BGCOLOR = BLACK
MARBLECOLOR = GREEN
BOARDCOLOR = RED
SELECTION = BLUE
BOARDSHADOWCOLOR = DARKRED
MARBLEHIGHLIGHTCOLOR = BLUE
TEXTCOLOR = BLACK
TEXTBGCOLOR = WHITE

pygame.init()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Random Board Game')

selectSound = pygame.mixer.Sound('Click.wav')
endGameSound = pygame.mixer.Sound('Ta Da.wav')

def main():
    playTutorial()
    DISPLAYSURF.fill(BGCOLOR)
    mousex, mousey = 0,0
    clicked = False
    selectedBox = None
    gameStatus = generateBoardData()
    gameStatus[3][3] = 0
    soundIndex = 0



    while True:
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard()
        placeMarbles(gameStatus)
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos

            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clicked = True



                if selectedBox == None:
                    selectedBox = getPositionInMatrix(mousex, mousey)

                    if selectedBox!=(None, None):
                        row1 = selectedBox[0]
                        col1 = selectedBox[1]
                        if gameStatus[row1][col1] == 1:
                            gameStatus[row1][col1] = 2
                            selectSound.play()
                        else:
                            selectedBox = None

                    else:
                        selectedBox = None

                else:
                    secondSelectiom = getPositionInMatrix(mousex, mousey)

                    if secondSelectiom!=(None, None):

                        row1 = selectedBox[0]
                        col1 = selectedBox[1]

                        row2 = secondSelectiom[0]
                        col2 = secondSelectiom[1]


                        if row1 == row2 and col1 == col2:
                            gameStatus[row1][col1] = 1
                            selectedBox = None
                            selectSound.play()



                        elif gameStatus[row2][col2] == 0:
                            if ((abs(row1-row2) == 2) != (abs(col1-col2) == 2)) and (row1 == row2 or col1 == col2):
                                middleCellRow = int((row1+row2)/2)
                                middleCellCol = int((col1+col2)/2)
                                if gameStatus[middleCellRow][middleCellCol] == 1:
                                    selectSound.play()
                                    gameStatus[row1][col1] = 0
                                    gameStatus[row2][col2] = 1
                                    gameStatus[middleCellRow][middleCellCol] = 0

                                selectedBox = None



        if isGameOver(gameStatus):
            score = countMarbles(gameStatus)

            printScore(score)

            if soundIndex == 0:
                soundIndex =1
                endGameSound.play()

            restartBox = printRestartOption()

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    x, y = event.pos
                    if restartBox.collidepoint(x,y):
                        DISPLAYSURF.fill(BLACK)
                        mousex, mousey = 0,0
                        clicked = False
                        selectedBox = None
                        gameStatus = generateBoardData()
                        gameStatus[3][3] = 0
                        soundIndex = 0


        pygame.display.update()



def generateBoardData():
    matrix = []

    for i in range(2):
        matrix.append([None, None, 1, 1, 1, None, None])

    for i in range(3, 6):
        matrix.append([1, 1, 1, 1, 1, 1, 1])

    for i in range(5, 7):
        matrix.append([None, None, 1, 1, 1, None, None])
    matrix[3][3] = 1
    return matrix

def centreOfMarbleInPixels(row, col):
    left = int((WINDOWWIDTH-2*BOARDRADIUS)/2)
    top = int((WINDOWHEIGHT-2*BOARDRADIUS)/2)

    x = GAP*(row+1) + MARBLERADIUS*(2*row+1) + left
    y = GAP*(col+1) + MARBLERADIUS*(2*col+1) + top

    return (x, y)

def drawBoard():
    matrix = generateBoardData()
    dimension = len(matrix)
    pygame.draw.circle(DISPLAYSURF, BOARDCOLOR, BOARDCENTRE, BOARDRADIUS)
    for i in range(dimension):
        for j in range(dimension):
            centre = centreOfMarbleInPixels(i, j)
            if matrix[i][j] != 0 and matrix[i][j] != None:
                pygame.draw.circle(DISPLAYSURF, BOARDSHADOWCOLOR, centre, MARBLERADIUS+5)


def placeMarbles(matrix):
    dimension = len(matrix)
    for i in range(dimension):
        for j in range(dimension):
            centre = centreOfMarbleInPixels(i, j)
            if matrix[i][j] == 2:
                pygame.draw.circle(DISPLAYSURF, MARBLEHIGHLIGHTCOLOR, centre, MARBLERADIUS+10, 10)
                pygame.draw.circle(DISPLAYSURF, MARBLECOLOR, centre, MARBLERADIUS)

            if matrix[i][j] == 1:
                pygame.draw.circle(DISPLAYSURF, MARBLECOLOR, centre, MARBLERADIUS)


def selectionGraphics(cell, num):
    centre = centreOfMarbleInPixels(cell[0], cell[1])
    if num ==1:
            pygame.draw.circle(DISPLAYSURF, BLUE, centre,MARBLERADIUS+10, 10)
    if num == 2:
        pygame.draw.circle(DISPLAYSURF, GREEN, centre,MARBLERADIUS+10, 10)



def getPositionInMatrix(x, y):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            centre = centreOfMarbleInPixels(i, j)
            top = centre[1]-MARBLERADIUS
            left = centre[0]-MARBLERADIUS
            temp = pygame.Rect(left, top, 2*MARBLERADIUS, 2*MARBLERADIUS)

            if temp.collidepoint(x, y):
                return (i, j)

    return (None, None)


def isMovePossible(matrix, row, col):
    dimension = len(matrix)
    if matrix[row][col] == 0 or matrix[row][col] == None:
        return False

    if row<dimension-2:
        nextCell_V = matrix[row+1][col]
        nextNextCell_V = matrix[row+2][col]
        if nextCell_V!=0 and nextCell_V!=None and nextNextCell_V==0:
            return True

    if row>2:
        prevCell_V = matrix[row-1][col]
        prevPrevCell_V = matrix[row-2][col]
        if prevCell_V!=0 and prevCell_V!=None and prevPrevCell_V==0:
            return True


    if col<dimension-2:
        nextCell_H = matrix[row][col+1]
        nextNextCell_H = matrix[row][col+2]
        if nextCell_H!=0 and nextCell_H!=None and nextNextCell_H==0:
            return True

    if col>2:
        prevCell_H = matrix[row][col-1]
        prevPrevCell_H = matrix[row][col-2]
        if prevCell_H!=0 and prevCell_H!=None and prevPrevCell_H==0:
            return True

    return False


def isGameOver(matrix):
    dimension = len(matrix)

    for i in range(dimension):
        for j in range(dimension):
            val = isMovePossible(matrix, i, j)
            if val:
                return False
    return True

def countMarbles(matrix):
    dimension = len(matrix)
    count = 0
    for i in range(dimension):
        for j in range(dimension):
            if matrix[i][j]!=0 and matrix[i][j]!=None:
                count+=1

    return count

def printScore(score):
    fontObj = pygame.font.Font('freesansbold.ttf', 32)
    textSurfObj = fontObj.render(("Score: %d" % score), True, TEXTCOLOR, TEXTBGCOLOR)
    textRectObj = textSurfObj.get_rect()
    textRectObj.center = (BOARDCENTRE[0], BOARDCENTRE[1])
    DISPLAYSURF.blit(textSurfObj, textRectObj)

def printRestartOption():
    restartFontObj = pygame.font.Font('freesansbold.ttf', 20)
    restartTextSurfObj = restartFontObj.render('click to restart', True, TEXTCOLOR, TEXTBGCOLOR)
    restartRectObj = restartTextSurfObj.get_rect()
    restartRectObj.center = (BOARDCENTRE[0], BOARDCENTRE[1]+BOARDRADIUS)
    DISPLAYSURF.blit(restartTextSurfObj, restartRectObj)

    return restartRectObj

def generateTutBoardData():
    matrix = []

    for i in range(2):
        matrix.append([None, None, 0, 0, 0, None, None])

    for i in range(3, 5):
        matrix.append([0, 0, 0, 0, 0, 0, 0])

    matrix. append([0,0,0,1,0,0,0])
    for i in range(5, 7):
        matrix.append([None, None, 1, 0, 0, None, None])
    matrix[3][3] = 1
    return matrix


def playTutorial():
    DISPLAYSURF.fill(WHITE)

    fontObj = pygame.font.Font('freesansbold.ttf', 20)
    textSurfObj = fontObj.render("Reduce the number of marbles as shown", True, TEXTCOLOR, TEXTBGCOLOR)
    textRectObj = textSurfObj.get_rect()
    textRectObj.center = (BOARDCENTRE[0], BOARDCENTRE[1]+50)

    pygame.display.update()
    pygame.time.wait(1000)
    tutGameStat = generateTutBoardData()
    tutGameStat[3][3] = 0
    drawBoard()
    DISPLAYSURF.blit(textSurfObj, textRectObj)
    placeMarbles(tutGameStat)
    pygame.display.update()
    pygame.time.wait(1000)
    selectionGraphics((6,2),1)
    selectSound.play()
    pygame.display.update()
    pygame.time.wait(1000)
    selectionGraphics((4,2),2)
    selectSound.play()
    pygame.display.update()
    pygame.time.wait(1000)
    tutGameStat[4][2] = 1
    tutGameStat[5][2] = 0
    tutGameStat[6][2] = 0
    drawBoard()
    DISPLAYSURF.blit(textSurfObj, textRectObj)
    placeMarbles(tutGameStat)
    pygame.display.update()
    pygame.time.wait(1000)
    selectionGraphics((4,3),1)
    selectSound.play()
    pygame.display.update()
    pygame.time.wait(1000)
    selectionGraphics((4,1),2)
    selectSound.play()
    pygame.display.update()
    pygame.time.wait(1000)
    tutGameStat[4][3] = 0
    tutGameStat[4][1] = 1
    tutGameStat[4][2] = 0
    drawBoard()
    DISPLAYSURF.blit(textSurfObj, textRectObj)
    placeMarbles(tutGameStat)
    pygame.display.update()
    pygame.time.wait(2000)



main()
