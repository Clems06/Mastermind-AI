#%%
from random import randint
import numpy as np

#Constants
number_to_color = {1: "#D90404", 2: "#05C7F2", 3: "#078C03", 4: "#F2B705", 5: "#F25C05", 6: "#F288A4", 7: "#4A2ABF",
                   8: "#606B73"}
color_to_number = {"#D90404": 1, "#05C7F2": 2, "#078C03": 3, "#F2B705": 4, "#F25C05": 5, "#F288A4": 6, "#4A2ABF": 7,
                   "#606B73": 8}
colors = {'red': "#D90404", 'blue': "#05C7F2", 'green': "#078C03", 'yellow': "#F2B705", 'orange': "#F25C05",
          'pink': "#F288A4", 'violet': "#4A2ABF", 'grey': "#606B73"}

#Initializations
def array_init(n):
    if n==1:
        return [np.array([i]) for i in range(1,9)]
    else:
        l = []
        for i in range(1,9):
            a = np.array([i])
            for _ in array_init(n-1):
                l.append(np.concatenate((a, _)))
        return l

def p_init(n):
    if n == 1:
        return [{i : (0,)} for i in range(1, 9)]
    else:
        l = []
        for d in p_init(n - 1):
            for k in range(1, 9):
                _=d.copy()
                if k in d:
                    _[k]+=(n-1,)
                else:
                    _[k]=(n-1,)
                l.append(_)
        return l

#Miscellaneous
def evaluate(pins1: dict, pins2: dict):
    w = 0
    r = 0
    for pin in pins1.keys():
        if pin in pins2:
            r_t = 0
            for i in pins1[pin]:
                r_t += int(i in pins2[pin])
            w += min(len(pins1[pin]), len(pins2[pin])) - r_t
            r += r_t
    return w, r

def todict(code: dict):
    d = {}
    for pin, i in zip(code,range(4)):
        if pin in d:
            d[pin] += (i,)
        else:
            d[pin] = (i,)
    return d

def tolist(code: dict):
    inv_map = {}
    for k, v in code.items():
        inv_map[v] = inv_map.get(v, []) + [k]
    return inv_map

def random_password():
    return todict({i : randint(1, 8) for i in range(4)})

class Board:
    def __init__(self, pwd = None):
        self.pwd = pwd or random_password()
        self.lines = []
        self.p = p_init(4)
        self.whites = []
        self.reds = []
        self.tries = 0

    def append(self, line):
        self.tries+=1
        self.lines.append(line)
        w, r = self.eval_input(line)
        self.whites.append(w)
        self.reds.append(r)
        self.p=[l for l in self.p if evaluate(l, line)==(w, r)]

    def eval_input(self, input: dict):
        return evaluate(self.pwd, input)

    def toinput(self):
        return np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]] + [toinput(line, w, r) for line, w, r in zip(self.lines, self.whites, self.reds)])
# %%