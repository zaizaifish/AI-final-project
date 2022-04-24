import sys
import random
import math
import argparse as ap
from utilities import run_simulation
from utilities.graphnode import node
from collections import defaultdict, deque
from heapq import heappop, heappush
from utilities.maze import *
SDL = True

name = "simulated annealing"

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

RUN = simulated_annealing

if __name__ == '__main__':
    a = ap.ArgumentParser(
        prog = 'simulatedannealing.py', 
        description = 'simple hill climbing algorithm implemented to solve a maze \
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
