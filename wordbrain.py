#!/usr/bin/python3

import wordDict

from collections import namedtuple
from copy import deepcopy

GRID = '''
NND
OTA
OIR
'''.lower()

GRIDPOS = namedtuple('GRIDPOS', 'row col val')
WORD_LENGTHS = [4, 5]

GRID = [list(x) for x in GRID.split() if len(x) > 0]
for i, row in enumerate(GRID):
    for j, cell in enumerate(row):
        print(i,j,cell)
        GRID[i][j] = GRIDPOS(i, j, cell)
MAX_COLS = MAX_ROWS = len(GRID) # Assuming a square

newGRID = [[GRIDPOS(row=0, col=0, val=None), GRIDPOS(row=0, col=1, val=None), GRIDPOS(row=0, col=2, val='d')], [GRIDPOS(row=1, col=0, val=None), GRIDPOS(row=1, col=1, val='b'), GRIDPOS(row=1, col=2, val='r')], [GRIDPOS(row=2, col=0, val=None), GRIDPOS(row=2, col=1, val='a'), GRIDPOS(row=2, col=2, val='e')]]
newWORD_LENGTHS = [5]


print("Making Word Tree")
WORDTREE = wordDict.wordtree()
print("Word Tree Done")

def explore_grid(grid=GRID, words_required=WORD_LENGTHS, answers=None):
    if answers is None:
        answers = []
    
    for row in grid:
        for cell in row:
            if cell.val is not None:
                current_test = [cell]
                #recurse!
                _explore_grid(grid, current_test, words_required, answers)
                
def _explore_grid(grid, current_test, words_required, answers=None):
    #should we continue this path?
    current_word = ''.join([x.val for x in current_test])
    #print(current_word)
    if not WORDTREE.prefix_valid(current_word):
        return False
    # do we have a word?
    if current_word in WORDTREE:
        #TODO: Worry about word lengths and multiword stuff
        if len(current_word) in words_required:
            answers.append(current_word)
            words_required.remove(len(current_word))
            if len(words_required) == 0:
                # We have an answer!
                print(answers)
            else:
                new_grid = update_copied_grid(grid, current_test)
                explore_grid(new_grid, words_required, answers)
            answers.pop()
            words_required.append(len(current_word))
    #check neighbours
    last_cell = current_test[-1]
    for x in range(max(last_cell.row-1,0),min(last_cell.row+2, MAX_ROWS)):
        for y in range(max(last_cell.col-1,0),min(last_cell.col+2, MAX_COLS)):
            if grid[x][y].val is not None and grid[x][y] not in current_test:
                current_test.append(grid[x][y])
                _explore_grid(grid, current_test, words_required, answers)
                current_test.pop()
    
def update_copied_grid(grid, to_remove):
    """updates the grid by taking in a list of GRIDPOS to remove, removing them
        and then letting all other blocks fall down"""
    grid = deepcopy(grid)
    # stage 1: remove the blocks
    for cell in to_remove:
        grid[cell.row][cell.col] = GRIDPOS(cell.row, cell.col, None)
        
    #stage 2: gravity
    for row in grid[::-1]:
        for cell in row:
            if cell.val is None:
                if cell.row > 0:
                    grid[cell.row][cell.col] = GRIDPOS(cell.row, cell.col, 
                                        grid[cell.row-1][cell.col].val)
                    grid[cell.row-1][cell.col] = GRIDPOS(cell.row-1, cell.col,
                                        None)
                else:
                    grid[cell.row][cell.col] = GRIDPOS(cell.row, cell.col,
                                        None)
                                         
    return grid
    

explore_grid()



















