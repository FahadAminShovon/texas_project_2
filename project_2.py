import sys
import copy
# sys.setrecursionlimit(10**6)
class NoStartPositionError(Exception):
    pass

class NoEndPositionError(Exception):
    pass

class FileEmptyError(Exception):
    pass

class UnSolveableError(Exception):
    pass

class InvalidCharecterError(Exception):
    pass

def errohandler(x,value,error,message):
    try:
        if x == value: raise error
    except error:
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

directions = "><^v"
class Maze:
    def __init__(self,state:list,sx,sy,ex,ey):
        self.state =  copy.deepcopy(state)
        self.sx,self.sy,self.ex,self.ey = sx,sy,ex,ey
        self.cx,self.cy = sx,sy
        # print(self.sx, self.sy)
        self.removeDuplicate()
        self.solutions = []

    def removeDuplicate(self):
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if self.state[i][j]=='S':
                    if i!=self.sx or j!=self.sy:
                        # print(i,j)
                        self.state[i][j]='#'

    def showCurrentMaze(self):
        for i in self.state:
            for j in i:
                print(j, end="")
            print()
        print()
        print("=" * len(self.state[0]), "\n")

    def showMaze(self):
        for state in self.solutions:
            for i in state:
                for j in i:
                    print(j,end="")
                print()
            print()
            print("="*len(state[0]),"\n")


    def is_open_path(self):
        row = self.cx
        col = self.cy
        state = self.state

        #print(row,col)

        for i in range(4):
            colx = col+xx[i]
            rowy = row+yy[i]
            #print(rowy,colx,state[rowy][colx])
            if colx>=0 and colx<len(state[row]) and rowy>=0 and rowy<len(state) and (state[rowy][colx]=='E' or state[rowy][colx]==' '):
                return True,rowy,colx,i
        return False,None,None,-1


    def reversable(self):
        row = self.cx
        col = self.cy
        state = self.state

        chh = state[row][col]
        if chh == 'S':
            return False,None,None
        if chh not in directions:
            return True,0,0
        res = directions.index(chh)

        colx = col+rxx[res]
        rowy = row+ryy[res]

        return True,rowy,colx


    def is_solved(self) ->bool :
        return  self.cx == self.ex and self.cy == self.ey

    def findSolution(self):
        self.solutions.append(copy.deepcopy(self.state))
        is_Open,rowy,colx,direction = self.is_open_path()
        if is_Open:
            self.cx,self.cy=rowy,colx
            if self.is_solved():
                return True
            self.state[self.cx][self.cy]=directions[direction]
            self.findSolution()
        hasSolution,rowy, colx = self.reversable()
        if hasSolution:
            if self.is_solved():
                return True
            self.state[self.cx][self.cy] = '.'
            self.cx, self.cy = rowy, colx
            self.findSolution()
        else:return False



def getMaze():
    try:
        maxx = 0
        f = open("test1.txt")
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
                errohandler(isValid(temp), False, InvalidCharecterError, "Error: Maze contains invalid characters. Line {} contains invalid character {}".format(row,temp))

        errohandler(em,0,FileEmptyError,"Error: Specified file contains no maze.")
        errohandler(s, 0, NoStartPositionError,"Error: No start position found.")
        errohandler(e, 0, NoEndPositionError,"Error: No end position found.")
        errohandler(sp, 0, UnSolveableError,"Error: No route could be found from start to end. Maze unsolvable.")

        for row in maze:
            while len(row)!=maxx:
                row.append(' ')
        mazes = []

        for i in range(len(sx)):
            mazes.append(Maze(maze,sx[i],sy[i],ex,ey))

    except FileNotFoundError:
        print("Error: Specified file does not exist.")

    return mazes

if __name__=="__main__":
    mazefile = getMaze()
    try:
        counter = 0

        for maze in mazefile:
            if maze.findSolution():
                maze.showMaze()
                counter+=1
        if counter==0:raise UnSolveableError
    except UnSolveableError:
        print("Error: No route could be found from start to end. Maze unsolvable.")
        sys.exit(1)


