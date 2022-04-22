import sys
import argparse as ap
import heapq
from heapq import heappop, heappush
from utilities import run_simulation
from utilities.graphnode import node
from collections import defaultdict
from utilities.maze import main, get_maze
SDL = True

name = "A* algorithm"

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
    res = []
    cur = goalstate
    while cur != startstate:
        res.append(cur)
        cur = parents[cur]
    res.append(startstate)
    res.reverse()
    return res, None

RUN = astar

if __name__ == '__main__':
    a = ap.ArgumentParser(
        prog = 'astar.py', 
        description = 'A* algorithm implemented to solve a maze problem', 
        epilog = 'Note: -c option is used with -s option'
    )
    a.add_argument(
        dest = 'mazefile', 
        help = 'the maze file containing maze to solve'
    )
    a.add_argument(
        '-s', 
        '--simulate', 
        dest = 'simulate', 
        help = 'provide if you want the graphical simulation of the path found by \
                algorithm in maze to be shown', 
        action = 'store_true')
    a.add_argument(
        '-c', 
        '--continuous', 
        dest = 'cont', 
        help = 'if supplied, the simulation is continuous (mouse click not \
                needed for each turn)', 
        action = 'store_true'
    )
    args = a.parse_args()
    m = get_maze(args.mazefile)
    if not m:
        print('error: invalid maze file provided', file = sys.stderr)
        sys.exit()
    if args.simulate:
        if SDL:
            run_simulation.run_simulation(
                name, 
                main(
                    RUN,
                    m, 
                    to_print = False
                ), 
                m, 
                continuous = args.cont
            )
        else:
            print("error: can't make simulation, PySDL2 not installed")
            print("printing path instead...")
            main(RUN, m, to_print = True)
    else:
        main(RUN, m, to_print = True)
