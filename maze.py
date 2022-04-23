SOLUTION_FOUND = 0x1
SOLUTION_NOT_FOUND = 0x2

class maze_t:
    '''maze data structure which holds the information of maze'''
    def __init__(self, data, row, col, start, goal):
        '''initialises maze'''
        self.r = row
        self.c = col
        self.data = data
        self.startstate = start
        self.goalstate = goal

    def __str__(self):
        '''gives the numeric representation of maze'''
        s = ""
        for i in self.data:
            s += str(i)
            s += "\n"
        return s 

    def nextstate(self, currentstate):
        '''gives the next states of maze'''
        res = []
        x, y = currentstate[0], currentstate[1]
        if x > 0 and self.data[x - 1][y] == 1:
            res.append((x - 1, y))
        if x < self.r - 1 and self.data[x + 1][y] == 1:
            res.append((x + 1, y))
        if y > 0 and self.data[x][y - 1] == 1:
            res.append((x, y - 1))
        if y < self.c - 1 and self.data[x][y + 1] == 1:
            res.append((x, y + 1))
        return res
    
    def value(self, state):
        '''heuristic function
        returns the value h(n) of a state'''
        return abs(self.goalstate[0] - state[0]) + abs(self.goalstate[1] - state[1])

    def is_better(self, s1, s2, toprint = False):
        '''function which tells if state s1 if better than state s2'''
        val1 = self.value(s1)
        val2 = self.value(s2)
        if val1 == val2:
            return s1[0] > s2[0]
        if toprint:
            print("{} : {} < {} : {}".format(s1, val1, s2, val2))
        return bool(val1 < val2)

def get_maze(filename):
    '''returns a maze from a filename'''
    f = open(filename, "r+", encoding = 'utf8')    
    matrix = []
    row, col = 0, 0
    start, goal = None, None
    for i in f.readlines():
        i = i.rstrip('\n')
        if 'row' in i:
            row = int(i.split(" ")[-1])
            print("row: ", row)
        elif 'col' in i:
            col = int(i.split(" ")[-1])
            print("col: ", col)
        elif 'start' in i:
            i = i.split(" ")
            start = (int(i[1]), int(i[2]))
            print("start: ", start)
        elif 'goal' in i:
            i = i.split(" ")
            goal = (int(i[1]), int(i[2]))
            print("goal: ", goal)
        else:
            print(i)
            matrix.append(i)
    data = [[1 if i == ' ' else 0 for i in j] for j in matrix]
    return maze_t(data, row, col, start, goal)

def main(fun, maze, to_print = True):
    '''a function which returns a path in {up, down, left, right} format
    parameters
    fun :       the function which applied a specific algorithm to the maze 
                and returns the coordinates list indicating the path
                the function also needs to return another value whether solution is found or not
                along with the path
    maze :      the maze_t instance (the maze to be solved)
    to_print :  whether to print the result or not'''
    path, _ = fun(maze)
    result_path = []
    if to_print:
        print("path to other end found")
    prev = None
    for cur in path:
        if prev is None: 
            result_path.append("start")
        elif cur[0] > prev[0]:
            result_path.append("down") 
        elif cur[0] < prev[0]:
            result_path.append("up") 
        elif cur[1] > prev[1]:
            result_path.append("right") 
        elif cur[1] < prev[1]:
            result_path.append("left")
        prev = cur
    result_path.append("end")
    if to_print:
        print(", ".join(result_path))
    return result_path

def make_path(start, goal, parents):
    res = []
    cur = goal
    while cur != start:
        res.append(cur)
        cur = parents[cur]
    res.append(start)
    res.reverse()
    return res