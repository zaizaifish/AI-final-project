import sys
import argparse as ap
from utilities import run_simulation
from utilities.graphnode import node
from collections import defaultdict
from utilities.maze import *
SDL = True

name = "Depth First Search"

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

RUN = dfs

if __name__ == '__main__':
    a = ap.ArgumentParser(
        prog = 'dfs.py', 
        description = 'depth first search algorithm implemented to solve a maze \
                problem', 
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
