import sys
import copy

def errohandler(x,value,message):
    if x == value:
        print(message)
        sys.exit(1)

def split(word):
    return [char for char in word]


def isValid(c):
    return  c in 'SE# ^>V^'

xx = [1,-1,0,0]
yy = [0,0,-1,1]
#right,left, up, down

rxx = [-1,1,0,0]
ryy = [0,0,1,-1]
#left,right,down,up

cx,cy = 0,0


directions = "><^v"

def solve(matrix,sx,sy,ex,ey):
    global cx,cy

    state = copy.deepcopy(matrix)
    cx,cy=sx,sy
    removeDuplicate(state,sx,sy)
    solutions = []
    if findSolution(solutions,state,ex,ey):
        showMaze(solutions)
        return




def removeDuplicate(state,sx,sy):
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 'S':
                if i != sx or j != sy:
                    state[i][j] = '#'


def showCurrentMaze(state):
    for i in state:
        for j in i:
            print(j, end="")
        print()
    print()
    print("=" * len(state[0]), "\n")



def showMaze(solutions):
    for state in solutions:
        for i in state:
            for j in i:
                print(j,end="")
            print()
        print()
        print("="*len(state[0]),"\n")

def is_open_path(state):
    global cx,cy
    row=cx
    col=cy
    for i in range(4):
        colx = col+xx[i]
        rowy = row+yy[i]
        if colx>=0 and colx<len(state[row]) and rowy>=0 and rowy<len(state) and (state[rowy][colx]=='E' or state[rowy][colx]==' '):
            return True,rowy,colx,i
    return False,None,None,-1


def reversable(state):
    global cx,cy
    row = cx
    col = cy

    chh = state[row][col]
    if chh == 'S':
        return False, None, None
    if chh not in directions:
        return True, 0, 0

    res = directions.index(chh)

    colx = col + rxx[res]
    rowy = row + ryy[res]

    return True, rowy, colx


def is_solved(ex,ey):
    global cx,cy
    return cx == ex and cy == ey

def findSolution(solutions,state,ex,ey):
    global cx,cy
    solutions.append(copy.deepcopy(state))
    #showMaze(solutions)
    is_Open, rowy, colx, direction = is_open_path(state)
    if is_Open:
        cx, cy = rowy, colx
        if is_solved(ex,ey):
            return True
        state[cx][cy] = directions[direction]
        findSolution(solutions,state,ex,ey)
    hasSolution, rowy, colx = reversable(state)
    if hasSolution:
        if is_solved(ex,ey):
            return True
        state[cx][cy] = '.'
        cx, cy = rowy, colx
        findSolution(solutions,state,ex,ey)
    else:
        return False



def getMaze():
    try:
        maxx = 0
        f = open("multiplestart.txt")
        maze = []
        while True:
            line = f.readline()
            if line:
                xx = split(line)
                if xx[-1] == '\n': xx.pop()
                if(maxx<len(xx)):maxx=len(xx)
                maze.append(xx)
            else:
                break
        s = 0
        e = 0
        em = 0
        sp = 0
        sx,sy,ex,ey = [],[],0,0

        for row in range(len(maze)):
            for col in range(len(maze[row])):
                temp = maze[row][col]
                em+=1
                if temp=='E':
                    e+=1
                    ex,ey=row,col
                elif temp=='S':
                    s+=1
                    sx.append(row)
                    sy.append(col)
                elif temp==' ':
                    sp+=1
                errohandler(isValid(temp), False, "Error: Maze contains invalid characters. Line {} contains invalid character {}".format(row,temp))

        errohandler(em,0,"Error: Specified file contains no maze.")
        errohandler(s, 0,"Error: No start position found.")
        errohandler(e, 0,"Error: No end position found.")
        errohandler(sp, 0,"Error: No route could be found from start to end. Maze unsolvable.")

        for row in maze:
            while len(row)!=maxx:
                row.append(' ')

        for i in range(len(sx)):
            solve(maze,sx[i],sy[i],ex,ey)

    except FileNotFoundError:
        print("Error: Specified file does not exist.")


if __name__=="__main__":
    mazefile = getMaze()



