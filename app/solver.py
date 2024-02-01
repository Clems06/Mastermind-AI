#%%
from environment import *
import numpy as np
import itertools
import time

P = {i:p_init(i) for i in range(1,5)}

def fast_eval(line1, line2, w):
    c = 0
    for pin in line1.keys():
        if pin in line2:
            for i in line1[pin]:
                if i in line2[pin]:
                    return False
            c += min(len(line1[pin]), len(line2[pin]))
    return w==c

def fast_gen(line, w, r, possibilities):
    l = []
    for comb_red in itertools.combinations(range(4), 4-r):
        red_l = todict([line[i] for i in range(4) if not i in comb_red])
        new_l = todict(line[list(comb_red)])
        for p in possibilities:
            if fast_eval(new_l, p, w):
                _ = red_l.copy()
                _.update(p)
                l.append(_)
    return l

"""
scores = np.zeros(5)
possibilities = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[]}
candidates = [np.array([1,1,1,1]),np.array([1,1,1,2]),np.array([1,1,2,2]),np.array([1,1,2,3]),np.array([1,2,3,4])]
for i, c in enumerate(candidates):
    n = 0
    d = todict(c)
    for password in P[4]:
        w, r = evaluate(d, password)
        if r==4:
            possibilities[i].append([password])
        else:
            possibilities[i].append(fast_gen(c, w, r, P[4-r]))
    for second_move in possibilities[i]:


print(possibilities[0][0])"""
s = time.time()
a = set(range(273))
b = set(range(273))
for i in range(5*300*15*15*15):
    b.intersection(a)
print(time.time()-s)