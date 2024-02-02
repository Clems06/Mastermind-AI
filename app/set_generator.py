#%%
import itertools
import numpy as np
import time
from environment import *

def blank_generator(white_pins, line, color_mask, placed_positions, banned_colors) -> set:
    """blank_generator(white_pins: dict, line: np.array, color_mask: dict, placed_positions: np.array, banned_colors: np.array)
    """
    rge = np.arange(line.size)
    #Captures cases when all white pins have been placed
    if len(white_pins)==0:
        colors = [[] for i in rge]
        #Computes the colors for each remaining pin
        for c in color_mask:
            value = color_mask[c]
            colors[c]=value[~np.in1d(value, banned_colors)]
        #Places the placed pins
        for placed in placed_positions:
            colors[placed] = [line[placed]]
        return set(itertools.product(*colors))
    else:
        B = set()
        white_pin = list(white_pins.items())[0]
        remaining_positions = np.setdiff1d(rge, placed_positions)
        for new_position, new_pin in zip(remaining_positions, line[remaining_positions]):
            if new_pin != white_pin[1]:
                new_color_mask=color_mask.copy()
                if white_pin[0] in new_color_mask:
                    new_color_mask[white_pin[0]][white_pin[1]-1]=0
                new_color_mask.pop(new_position)
                new_line = line.copy()
                new_line[new_position] = white_pin[1]
                new_placed_positions = np.concatenate((placed_positions, [new_position]))
                #Gets every possible placement with white_pin placed in placed_position
                B.update(blank_generator({i[0]:i[1] for i in white_pins.items() if i[0]!=white_pin[0]}, new_line, new_color_mask, new_placed_positions, banned_colors))
        return B

def white_generator(line, w) -> set:
    """white_generator(line: np.array, w: int) -> W: set
    line : remaining line when excluding red pins
    w : Number of white pins
    
    Returns the set containing all combinations for which line would be evaluated with w whites"""

    W = set()
    rge = np.arange(line.size)
    d = {i:np.arange(1,9) for i in rge}
    #Iterates over every possible white combination
    for white_positions in itertools.combinations(rge, w):
        #Gets all forbidden colors
        if w>0:
            mask = np.ones(line.size, np.bool_)
            mask[list(white_positions)] = 0
            banned_colors = np.concatenate((line[mask], [0]))
        else:
            banned_colors = np.concatenate((line, [0]))
        #Adds every final combination (excluding reds) to set
        for combinations in blank_generator({i:line[i] for i in white_positions}, line.copy(), d.copy(), np.empty(0, dtype=np.int8), banned_colors):
            W.add(combinations)
    return W

def generator(line, w, r) -> set:
    """generator(line: np.array, w: int, r: int) -> S: set
    line : input line
    w : number of white pins
    r : number of red pins
    
    Returns the set containing all passwords for which line would be evaluated with w whites and r reds"""

    S = set()
    rge = range(4)
    # Iterates over every possible red combination
    for remaining_positions in itertools.combinations(rge, 4 - r):
        #Gets remaining pins
        remaining_positions = list(remaining_positions)
        remaining_pins = line[remaining_positions]
        mask = np.ones(line.size, np.bool_)
        mask[remaining_positions] = 0
        #Iterates over every possible white combination
        for white_combinations in white_generator(remaining_pins, w):
            #Adds every final combination possible to set
            final_combination = np.zeros(4, dtype=np.int8)
            final_combination[remaining_positions] = white_combinations
            final_combination = np.sum([final_combination, np.multiply(line, mask)], axis=0)
            S.add(tuple(final_combination))
    return S

def classic_gen(line, w, r):
    return {tuple(p) for p in array_init(4) if evaluate(todict(p), todict(line))==(w, r)}

s = time.time()
"""for i, p in enumerate(array_init(4)[:1000]):
    classic_gen(list(p), 0, 2)
print(time.time()-s)"""
#20 secondes pour 1000
s = time.time()
"""for i, p in enumerate(array_init(4)[:1000]):
    generator(p, 3, 0)
print(time.time()-s)"""