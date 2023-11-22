#%%
class Line:
    def __init__(self, pins:dict, r_colour:int, r_place:int):
        self.code=pins
        self.w=r_colour
        self.r=r_place

class Board:
    def __init__(self, name:str, pwd:dict):
        self.name=name
        self.pwd=pwd
        self.lines=[]
        self.p=p_init(self.pwd)

    def l_append(self, line:Line):
        self.lines.append(line)
        self.p_update(line)

    def eval_input(self, input:dict):
        return evaluate(self.pwd, input)
    
    def append(self, input:dict):
        w,r=self.eval_input(input)
        self.l_append(Line(input, w, r))

    def p_update(self, line:Line):
        w,r=line.w, line.r
        for p in self.p:
            if (p.w,p.r)!=(w,r):
                self.p.remove(p)

def p_init(pwd:tuple):
    def d_gen(n):
        c=[{1:(0,)},{2:(0,)},{3:(0,)},{4:(0,)},{5:(0,)},{6:(0,)},{7:(0,)},{8:(0,)}]
        if n==1:
            return c
        else:
            l=[]
            for d in d_gen(n-1):
                for k in range(1,9):
                    d_t=d.copy()
                    if k in d_t:
                        d_t[k]+=(n-1,)
                    else:
                        d_t[k]=(n-1,)
                    l.append(d_t)
            return l
    return [Line(d, *evaluate(d,pwd)) for d in d_gen(4)]

def evaluate(pins1:dict, pins2:dict):
    w=0
    r=0
    for pin in pins1.keys():
        if pin in pins2:
            r_t=0
            for i in pins1[pin]:
                r_t+=int(i in pins2[pin])
            w+=min(len(pins1[pin]),len(pins2[pin]))-r_t
            r+=r_t
    return w,r

def todict(code:tuple):
    d={}
    for pin, i in zip(code,range(4)):
        if pin in d:
            d[pin]+=(i,)
        else:
            d[pin]=(i,)
    return d
    #%%