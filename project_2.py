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


def split(word):
    return [char for char in word]


def isValid(c):
    return  c in 'SE# ^>V^'

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


        for i in range(len(maze)):
            for j in range(len(maze[i])):
                temp = maze[i][j]
                em+=1
                if temp=='E':
                    e+=1
                elif temp=='S':
                    s+=1
                elif temp==' ':
                    sp+=1

                try:
                    if isValid(temp)==False:raise InvalidCharecterError
                except InvalidCharecterError:
                    print("Error: Maze contains invalid characters. Line {} contains invalid character {}".format(i,temp))
                    sys.exit(1)

        try:
            if em == 0:raise FileEmptyError
        except FileEmptyError:
            print("Error: Specified file contains no maze.")
            sys.exit(1)

        try:
            if s == 0:raise NoStartPositionError
        except NoStartPositionError:
            print("Error: No start position found.")
            sys.exit(1)

        try:
            if e == 0:raise NoEndPositionError
        except NoEndPositionError:
            print("Error: No end position found.")
            sys.exit(1)

        try:
            if sp == 0:raise UnSolveableError
        except UnSolveableError:
            print("Error: No route could be found from start to end. Maze unsolvable.")
            sys.exit(1)






    except FileNotFoundError:
        print("Error: Specified file does not exist.")

