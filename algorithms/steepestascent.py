import sys
import argparse as ap
from utilities import run_simulation
from utilities.graphnode import node
from collections import defaultdict, deque
from utilities.maze import *
SDL = True
name = "steepest ascent hill climbing"

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
        if beststate:
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

RUN = steepest_ascent_hill_climbing

if __name__ == '__main__':
    a = ap.ArgumentParser(
        prog = 'steepestascent.py', 
        description = 'simple hill climbing algorithm implemented to solve a \
                maze problem',
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
