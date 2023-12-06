from random import randint
import numpy as np

def p_init(n):
    c = [{1: (0,)}, {2: (0,)}, {3: (0,)}, {4: (0,)}, {5: (0,)}, {6: (0,)}, {7: (0,)}, {8: (0,)}]
    if n == 1:
        return c
    else:
        l = []
        for d in p_init(n - 1):
            for k in range(1, 9):
                d_t = d.copy()
                if k in d_t:
                    d_t[k] += (n - 1,)
                else:
                    d_t[k] = (n - 1,)
                l.append(d_t)
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


def todict(code: tuple):
    d = {}
    for pin, i in zip(code, range(4)):
        if pin in d:
            d[pin] += (i,)
        else:
            d[pin] = (i,)
    return d


def tolist(code: dict):
    l = [0, 0, 0, 0]
    for pin in code.items():
        for n in pin[1]:
            l[n] = pin[0]
    return tuple(l)


def random_password():
    return todict(tuple([randint(1, 8) for i in range(4)]))


BINARY = {1:[0,0,0],2:[0,0,1],3:[0,1,0],4:[0,1,1],5:[1,0,0],6:[1,0,1],7:[1,1,0],8:[1,1,1]}

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

    def append(self, line):
        self.lines.append(line)
        w, r = self.eval_input(line)
        self.p=[l for l in self.p if evaluate(l, line)==(w, r)]

    def eval_input(self, input: dict):
        return evaluate(self.pwd, input)

    def toinput(self):
        return np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]] + [toinput(line, *self.eval_input(line)) for line in self.lines])


number_to_color = {1: "#D90404", 2: "#05C7F2", 3: "#078C03", 4: "#F2B705", 5: "#F25C05", 6: "#F288A4", 7: "#4A2ABF",
                   8: "#606B73"}
color_to_number = {"#D90404": 1, "#05C7F2": 2, "#078C03": 3, "#F2B705": 4, "#F25C05": 5, "#F288A4": 6, "#4A2ABF": 7,
                   "#606B73": 8}
colors = {'red': "#D90404", 'blue': "#05C7F2", 'green': "#078C03", 'yellow': "#F2B705", 'orange': "#F25C05",
          'pink': "#F288A4", 'violet': "#4A2ABF", 'grey': "#606B73"}
# %%