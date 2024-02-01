#%%
from random import randint
import numpy as np

BINARY = {1:[0,0,0],2:[0,0,1],3:[0,1,0],4:[0,1,1],5:[1,0,0],6:[1,0,1],7:[1,1,0],8:[1,1,1]}
number_to_color = {1: "#D90404", 2: "#05C7F2", 3: "#078C03", 4: "#F2B705", 5: "#F25C05", 6: "#F288A4", 7: "#4A2ABF",
                   8: "#606B73"}
color_to_number = {"#D90404": 1, "#05C7F2": 2, "#078C03": 3, "#F2B705": 4, "#F25C05": 5, "#F288A4": 6, "#4A2ABF": 7,
                   "#606B73": 8}
colors = {'red': "#D90404", 'blue': "#05C7F2", 'green': "#078C03", 'yellow': "#F2B705", 'orange': "#F25C05",
          'pink': "#F288A4", 'violet': "#4A2ABF", 'grey': "#606B73"}

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

def toinput(code, w, r):
    output = [0 for _ in range(12)] + [w/4, r/4, 0]
    for pin in code.items():
        for n in pin[1]:
            output = output[:3*n] + BINARY[pin[0]] + output[3*n+3:]
    return output

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

def play_game(individual, tries_limit:int, opening=0, board=Board(), return_board = False):
    opening_moves=[]
    for coup in range(tries_limit):
        inputs = board.toinput()
        output = individual.get_output(inputs) / 2 + 0.5
        encoded_output = tuple([round(output[i])*4+round(output[i+1])*2+round(output[i+2])+1 for i in range(0, 10, 3)])
        if coup<opening:
            opening_moves.append(encoded_output)
        encoded_output = todict(encoded_output)
        board.append(encoded_output)
        if encoded_output == board.pwd:
            if return_board:
                return board
            return -coup*100, opening_moves
        elif len(board.p) == 1:
            if return_board:
                return board
            return -(coup+1) * 100, opening_moves
    if return_board:
        return board
    return -len(board.p)-tries_limit*100, opening_moves

def get_best_gen(contents):
    biggest = 0
    for file_content in contents:
        if file_content.type == "dir":
            biggest = max(int(file_content.path.split("_")[-1]), biggest)
    return biggest
# %%