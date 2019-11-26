import sys
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
yy = [0,0,1,-1]

class Maze:
    def __init__(self,state:list,sx,sy,ex,ey):
        self.state =  state
        self.sx,self.sy,self.ex,self.ey = sx,sy,ex,ey
        self.cx,self.cy = sx,sy

    def showMaze(self):
        for i in self.state:
            for j  in i:
                print(j,end="")
            print()
        print()
        print("="*len(self.state[0]),"\n")

    def is_open_path(self):
        cx = self.cx
        cy = self.cy
        state = self.state

        for i in range(4):
            tx = cx+xx
            ty = cy+yy

            if tx>=0 and tx<len(state[cx]) and ty>=0 and ty<len(state) and state[tx][ty]==" ":
                return True,tx,ty
        return False,None,None


    def is_solved(self) ->bool :
        return  self.cx == self.ex and self.cy == self.ey

    def findSolution(self):
        self.showMaze()
        if self.is_solved():
            return
        self.findSolution()



def getMaze():
    try:
        f = open("test1.txt")
        maze = []
        while True:
            line = f.readline()
            if line:
                xx = split(line)
                if xx[-1] == '\n': xx.pop()
                maze.append(xx)
            else:
                break
        s = 0
        e = 0
        em = 0
        sp = 0
        sx,sy,ex,ey = 0,0,0,0

        for i in range(len(maze)):
            for j in range(len(maze[i])):
                temp = maze[i][j]
                em+=1
                if temp=='E':
                    e+=1
                    ex,ey=i,j
                elif temp=='S':
                    s+=1
                    sx,sy=i,j
                elif temp==' ':
                    sp+=1
                errohandler(isValid(temp), False, InvalidCharecterError, "Error: Maze contains invalid characters. Line {} contains invalid character {}".format(i,temp))

        errohandler(em,0,FileEmptyError,"Error: Specified file contains no maze.")
        errohandler(s, 0, NoStartPositionError,"Error: No start position found.")
        errohandler(e, 0, NoEndPositionError,"Error: No end position found.")
        errohandler(sp, 0, UnSolveableError,"Error: No route could be found from start to end. Maze unsolvable.")

    except FileNotFoundError:
        print("Error: Specified file does not exist.")

    return Maze(maze,sx,sy,ex,ey)

mazefile = getMaze()
mazefile.findSolution()





