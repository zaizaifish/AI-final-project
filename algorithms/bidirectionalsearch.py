import sys
import argparse as ap
from utilities import run_simulation
from utilities.graphnode import node
from collections import defaultdict, deque
from utilities.maze import *
SDL = True

name = "bidirectional search"

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

RUN = bidirectional_both_bfs

if __name__ == '__main__':
    a = ap.ArgumentParser(
        prog = 'bidirectionalsearch.py', 
        description = 'bidirectional search algorithm implemented to solve a maze \
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
