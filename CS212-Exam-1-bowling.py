"""
UNIT 4: Search

Your task is to maneuver a car in a crowded parking lot. This is a kind of 
puzzle, which can be represented with a diagram like this: 

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O . . . A A |  
| O . S S S . |  
| | | | | | | | 

A '|' represents a wall around the parking lot, a '.' represents an empty square,
and a letter or asterisk represents a car.  '@' marks a goal square.
Note that there are long (3 spot) and short (2 spot) cars.
Your task is to get the car that is represented by '**' out of the parking lot
(on to a goal square).  Cars can move only in the direction they are pointing.  
In this diagram, the cars GG, AA, SSS, and ** are pointed right-left,
so they can move any number of squares right or left, as long as they don't
bump into another car or wall.  In this diagram, GG could move 1, 2, or 3 spots
to the right; AA could move 1, 2, or 3 spots to the left, and ** cannot move 
at all. In the up-down direction, BBB can move one up or down, YYY can move 
one down, and PPP and OO cannot move.

You should solve this puzzle (and ones like it) using search.  You will be 
given an initial state like this diagram and a goal location for the ** car;
in this puzzle the goal is the '@' empty spot in the wall on the right side.
You should return a path -- an alternation of states and actions -- that leads
to a state where the car overlaps the goal.

An action is a move by one car in one direction (by any number of spaces).  
For example, here is a successor state where the AA car moves 3 to the left:

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O A A . . . |  
| O . . . . . |  
| | | | | | | | 

And then after BBB moves 2 down and YYY moves 3 down, we can solve the puzzle
by moving ** 4 spaces to the right:

| | | | | | | |
| G G . . . . |
| P . . . . . |
| P . . . . * *
| P . . B . Y |
| O A A B . Y |
| O . . B . Y |
| | | | | | | |

You will write the function

    solve_parking_puzzle(start, N=N)

where 'start' is the initial state of the puzzle and 'N' is the length of a side
of the square that encloses the pieces (including the walls, so N=8 here).

We will represent the grid with integer indexes. Here we see the 
non-wall index numbers (with the goal at index 31):

 |  |  |  |  |  |  |  |
 |  9 10 11 12 13 14  |
 | 17 18 19 20 21 22  |
 | 25 26 27 28 29 30 31
 | 33 34 35 36 37 38  |
 | 41 42 43 44 45 46  |
 | 49 50 51 52 53 54  |
 |  |  |  |  |  |  |  |

The wall in the upper left has index 0 and the one in the lower right has 63.
We represent a state of the problem with one big tuple of (object, locations)
pairs, where each pair is a tuple and the locations are a tuple.  Here is the
initial state for the problem above in this format:
"""

import unittest
from pprint import pprint
puzzle1 = (
 ('@', (31,)),
 ('*', (26, 27)), 
 ('G', (9, 10)),
 ('Y', (14, 22, 30)), 
 ('P', (17, 25, 33)), 
 ('O', (41, 49)), 
 ('B', (20, 28, 36)), 
 ('A', (45, 46)), 
 ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39,
        40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)))

# A solution to this puzzle is as follows:

#     path = solve_parking_puzzle(puzzle1, N=8)
#     path_actions(path) == [('A', -3), ('B', 16), ('Y', 24), ('*', 4)]

# That is, move car 'A' 3 spaces left, then 'B' 2 down, then 'Y' 3 down, 
# and finally '*' moves 4 spaces right to the goal.

# Your task is to define solve_parking_puzzle:

N = 8

def find_in_state(needle, haystack):
    for (o, loc) in haystack:
        if o == needle: return loc

def collision(loc, state, our_car=False):
    for (o, oloc) in state:
        if our_car and o == '@': continue
        for pos in loc:
            if pos in oloc: return True
        
    return False

def move_car(car, delta):
    return tuple(p + delta for p in car)

def parking_goal(state):
    return True if find_in_state('@', state)[0] in find_in_state('*', state) else False

def parking_moves(state, car):
    label, loc = car
    delta = loc[1] - loc[0] #determine delta, if L/R delta == 1, if U/D delta == 8
    clearstate = set(state) - set([car]) # a state with the car removed
    
    moves = []
    moveby = -1
    nloc = move_car(loc, moveby * delta)
    while not collision(nloc, clearstate, label=='*'):
        moves.append((moveby * delta, nloc))
        moveby -= 1
        nloc = move_car(loc, moveby * delta)
    
    moveby = 1
    nloc = move_car(loc, moveby * delta)
    while not collision(nloc, clearstate, label=='*'):
        moves.append((moveby * delta, nloc))
        moveby += 1
        nloc = move_car(loc, moveby * delta)
    
    return [(tuple(clearstate | set([(label, mloc)])), (label, d)) for d, mloc in moves]

def parking_successors(state):
    #for car, loc in state:
    #    for action, newstate in parking_moves(state, car, loc):
    #        print action, newstate
    return dict((action,newstate) for car, loc in state if car != '@' and car != '|'
                for (action, newstate) in parking_moves(state, (car, loc)))

def solve_parking_puzzle(start, N=N):
    """Solve the puzzle described by the starting position (a tuple 
    of (object, locations) pairs).  Return a path of [state, action, ...]
    alternating items; an action is a pair (object, distance_moved),
    such as ('B', 16) to move 'B' two squares down on the N=8 grid."""
    return shortest_path_search(start, parking_successors, parking_goal)
    
# But it would also be nice to have a simpler format to describe puzzles,
# and a way to visualize states.
# You will do that by defining the following two functions:

def locs(start, n, incr=1):
    "Return a tuple of n locations, starting at start and incrementing by incr."
    return tuple(x for x in range(start, start+incr*n, incr))

def grid(cars, N=N):
    """Return a tuple of (object, locations) pairs -- the format expected for
    this puzzle.  This function includes a wall pair, ('|', (0, ...)) to 
    indicate there are walls all around the NxN grid, except at the goal 
    location, which is the middle of the right-hand wall; there is a goal
    pair, like ('@', (31,)), to indicate this. The variable 'cars'  is a
    tuple of pairs like ('*', (26, 27)). The return result is a big tuple
    of the 'cars' pairs along with the walls and goal pairs."""
    goal = ('@', locs(N*N/2-1, 1))
    walls = ('|', locs(0, N-1) + locs(N, N-1, N) + 
             locs(N*(N-1), N-1) + locs(N-1, (N/2)-1, N) + locs((N*(N/2+1)) - 1, N/2, N))
    
    return (goal, walls) + tuple(car for car in cars)

def show(state, N=N):
    "Print a representation of a state as an NxN grid."
    # Initialize and fill in the board.
    board = ['.'] * N**2
    for (c, squares) in state:
        for s in squares:
            #print s
            board[s] = c
    # Now print it out
    for i,s in enumerate(board):
        print s,
        if i % N == N - 1: print

# Here we see the grid and locs functions in use:

puzzle1 = grid((
    ('*', locs(26, 2)),
    ('G', locs(9, 2)),
    ('Y', locs(14, 3, N)),
    ('P', locs(17, 3, N)),
    ('O', locs(41, 2, N)),
    ('B', locs(20, 3, N)),
    ('A', locs(45, 2))))

puzzle2 = grid((
    ('*', locs(26, 2)),
    ('B', locs(20, 3, N)),
    ('P', locs(33, 3)),
    ('O', locs(41, 2, N)),
    ('Y', locs(51, 3))))

puzzle3 = grid((
    ('*', locs(25, 2)),
    ('B', locs(19, 3, N)),
    ('P', locs(36, 3)),
    ('O', locs(45, 2, N)),
    ('Y', locs(49, 3))))

# Here are the shortest_path_search and path_actions functions from the unit.
# You may use these if you want, but you don't have to.

def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set() # set of states we have visited
    frontier = [ [start] ] # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
                    #show(state)
    return []

def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

class Test(unittest.TestCase):
    def test_locs(self):
        self.assertEqual(locs(26, 2), (26, 27), 'locs broken')
        self.assertEqual(locs(26, 3), (26, 27, 28), 'locs broken')
        self.assertEqual(locs(26, 2, 8), (26, 34), 'locs broken')
        
    def test_goal(self):
        self.assertTrue(parking_goal((('@', (31,)), ('*', (30, 31)))), 'not detecting goal')
        self.assertFalse(parking_goal((('@', (31,)), ('*', (29, 30)))), 'incorrectly detecting goal')
        
    def test_collision(self):
        self.assertTrue(collision( (0,1), ( ('*', (1, 2)), ) ), 'missed collision')
        self.assertFalse(collision((0,1), ( ('*', (2, 3)),) ), 'reporting incorrect collision')
        
    def test_move_car(self):
        self.assertEqual(move_car((4,5), -1), (3,4), 'move incorrect')
        self.assertEqual(move_car((4,5), 1), (5,6), 'move incorrect')
        self.assertEqual(move_car((10,18), 8), (18,26), 'move incorrect')

#show(puzzle1)

#pprint(parking_successors(puzzle1))
#print path_actions(solve_parking_puzzle(puzzle1))