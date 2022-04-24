import sys
import argparse as ap
import random
from types import SimpleNamespace
from collections import defaultdict, deque
from heapq import heappop, heappush
from maze import *
try:
    import run_simulation
    SDL = True
except ImportError:
    SDL = False

# ==============================================================================
# 1. Simple algorithm                                                          |
# ==============================================================================
def simple_hill_climbing(maze):
    currentstate = maze.startstate
    startstate = maze.startstate
    goalstate = maze.goalstate
    path = [currentstate]
    parents = {}
    def backtrack(currentstate):
        if currentstate == goalstate: return True ### found goal
        temp = []
        for state in maze.nextstate(currentstate):
            if maze.is_better(state, currentstate):
                if state not in parents:
                    parents[state] = currentstate
                    res = backtrack(state)
                    if res: return res
            else: 
                if state not in parents:
                    temp.append(state)
        for state in temp:
            parents[state] = currentstate
            res = backtrack(state)
            if res: return res
    backtrack(currentstate)
    res_path = make_path(startstate, goalstate, parents)
    return res_path, None

# ==============================================================================
# 2. A* algorithm                                                              |
# ==============================================================================
def is_better_present_in_list(cost, state, d):
    '''returns True is a better state than the given state is present in
    mylist self'''
    if state in d:
        if d[state] <= cost:
            return True
    return False

def astar(maze):
    goalstate = maze.goalstate
    startstate = maze.startstate
    OPEN = []
    OPEN_DICT = {}
    CLOSED = []
    CLOSED_DICT = {}
    heappush(OPEN, (0, startstate))
    OPEN_DICT[startstate] = 0
    parents = {}
    while OPEN:
        g, q = heappop(OPEN)
        OPEN_DICT.pop(q)
        for state in maze.nextstate(q):
            if state == goalstate:
                parents[state] = q
                break
            h = 1
            f = g + h
            if is_better_present_in_list(f, state, OPEN_DICT):
                continue
            if is_better_present_in_list(f, state, CLOSED_DICT):
                continue
            parents[state] = q
            heappush(OPEN, (f, state))
            OPEN_DICT[state] = f
        heappush(CLOSED, (g, q))
        CLOSED_DICT[q] = g

    ### retrieve path
    res = make_path(startstate, goalstate, parents)
    return res, None

# ==============================================================================
# 3. bfs algorithm                                                             |
# ==============================================================================
def bfs(maze):
    startstate = maze.startstate
    goalstate = maze.goalstate
    queue = deque([startstate])
    visited = defaultdict(tuple)
    while len(queue) > 0:
        cur = queue.popleft()
        if cur == goalstate: break
        for next_state in maze.nextstate(cur):
            if not visited[next_state]:
                queue.append(next_state)
                visited[next_state] = cur
    res = make_path(startstate, goalstate, visited)
    return res, None

# ==============================================================================
# 4. dfs algorithm                                                             |
# ==============================================================================
def dfs(maze):
    startstate = maze.startstate
    goalstate = maze.goalstate
    stack = [startstate]
    visited = defaultdict(tuple)
    while len(stack) > 0:
        cur = stack.pop()
        if cur == goalstate: break
        for next_state in maze.nextstate(cur):
            if not visited[next_state]:
                stack.append(next_state)
                visited[next_state] = cur
    res = make_path(startstate, goalstate, visited)
    return res, None

# ==============================================================================
# 5. Bidirectional Search algorithm                                            |
# ==============================================================================
def bidirectional_both_bfs(maze):
    startstate = maze.startstate
    goalstate = maze.goalstate
    queue1 = deque([startstate])
    visited1 = defaultdict(tuple)
    queue2 = deque([goalstate])
    visited2 = defaultdict(tuple)
    intersect = None
    while len(queue1) > 0 and len(queue2) > 0:
        cur1 = queue1.popleft()
        cur2 = queue2.popleft()
        if cur1 in visited2: 
            intersect = cur1
            break
        if cur2 in visited1: 
            intersect = cur2
            break
        for next_state in maze.nextstate(cur1):
            if not visited1[next_state]:
                queue1.append(next_state)
                visited1[next_state] = cur1
        for next_state in maze.nextstate(cur2):
            if not visited2[next_state]:
                queue2.append(next_state)
                visited2[next_state] = cur2
    res1 = make_path(startstate, intersect, visited1)
    res2 = make_path(goalstate, visited2[intersect], visited2)
    res2.reverse()
    return res1 + res2, None

# ==============================================================================
# 6. Simmulated Annealing algorithm                                            |
# ==============================================================================
def simulated_annealing(maze):
    T = 200
    k = 1e-2
    random.seed(1024)
    currentstate = maze.startstate
    startstate = maze.startstate
    goalstate = maze.goalstate
    path = [currentstate]
    parents = {}
    def backtrack(currentstate):
        E1 = maze.value(currentstate)
        if currentstate == goalstate: return True ### found goal
        temp = []
        for state in maze.nextstate(currentstate):
            E2 = maze.value(state)
            if maze.is_better(state, currentstate):
                if state not in parents:
                    parents[state] = currentstate
                    res = backtrack(state)
                    if res: return res
            else: 
                if state not in parents:
                    p = 0
                    try:
                        p = math.e ** (- ((E2 - E1) / (k * T)))
                        T *= 0.9 
                    except:
                        p = 1
                    if p < random.random():
                        parents[state] = currentstate
                        res = backtrack(state)
                        if res: return res
                    else:
                        temp.append(state)
        for state in temp:
            parents[state] = currentstate
            res = backtrack(state)
            if res: return res
    backtrack(currentstate)
    res_path = make_path(startstate, goalstate, parents)
    return res_path, None

# ==============================================================================
# 7. Steepest Descent algorithm                                                |
# ==============================================================================
def steepest_ascent_hill_climbing(maze):
    currentstate = maze.startstate
    startstate = maze.startstate
    goalstate = maze.goalstate
    path = [currentstate]
    parents = {}
    def backtrack(currentstate):
        if currentstate == goalstate: return True ### found goal
        temp = []
        beststate, best = None, maze.value(currentstate)
        for state in maze.nextstate(currentstate):
            if maze.value(state) < best:
                if state not in parents:
                    best, beststate = maze.value(state), state
        for state in maze.nextstate(currentstate):
            if state != beststate:
                temp.append(state)
        if (beststate):
            parents[beststate] = currentstate
            res = backtrack(beststate)
            if res: return res
        for state in temp:
            if state not in parents:
                parents[state] = currentstate
                res = backtrack(state)
                if res: return res
    backtrack(currentstate)
    res_path = make_path(startstate, goalstate, parents)
    return res_path, None


################################################################################

all_list = [simple_hill_climbing, astar, bfs, dfs, bidirectional_both_bfs, \
            simulated_annealing, steepest_ascent_hill_climbing]
totals = len(all_list)

def get_parsed_arguments():
    if '-l' in sys.argv or '--list' in sys.argv:
        return SimpleNamespace(show_list = True)
    a = ap.ArgumentParser(
        prog = 'run.py', 
        description = 'driver program implemented to solve a maze \
            problem with any algorithm', 
        epilog = 'Note: -c option is used with -s option'
    )
    a.add_argument(
        '-l', 
        '--list',
        dest = 'show_list',
        help = 'shows the list of total algorithms which can be \
            used for solving a particular maze', 
        action = 'store_true'
    )
    a.add_argument(
        dest = 'mazefile', 
        help = 'the maze file containing maze to solve'
    )
    a.add_argument(
        '-s', 
        '--simulate', 
        dest = 'simulate', 
        help = 'provide if you want the graphical simulation of the \
            path found by algorithm in maze to be shown (must have \
            PySDL2 module on your pc)', 
        action = 'store_true'
    )
    a.add_argument(
        '-c', 
        '--continuous', 
        dest = 'cont', 
        help = 'if supplied, the simulation is continuous (mouse \
            click not needed for each turn, PySDL2 module required)', 
        action = 'store_true'
    )
    a.add_argument(
        '-a', 
        '--algorithm', 
        dest = 'al', 
        type = int, 
        help = 'decide which method to use for solving the maze (for \
            example, 1 for simple hill climbing) for a list of total \
            methods use -l or --list option', 
        default = 1, 
        choices = list(range(1, totals + 1))
    )
    return a.parse_args()


def run():
    args = get_parsed_arguments()
    if args.show_list:
        print("total algorithms:")
        for no, alg in enumerate(all_list, 1):
            print("\t%d\t%s" %(no, alg.__name__))
    else:
        m = get_maze(args.mazefile)
        if not m:
            print('error: invalid maze file provided', file = sys.stderr)
            return -1
        print(
            "using %s algorithm on maze..." 
            %(all_list[args.al - 1].__name__)
        )
        printpath = False
        if args.simulate:
            if SDL:
                run_simulation.run_simulation(
                    all_list[args.al - 1], 
                    main(
                        all_list[args.al - 1], 
                        m, 
                        to_print = False
                    ), 
                    m, 
                    continuous = args.cont
                )
            else:
                print("error: can't make simulation, PySDL2 not installed")
                print("printing path instead...")
                printpath = True
        else:
            printpath = True
        if printpath:
            print()
            main(all_list[args.al - 1], m, to_print = True)
    return 0

if __name__ == '__main__':
    sys.exit(run())
