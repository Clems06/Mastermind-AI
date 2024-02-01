from flask import Flask, render_template, request, session, jsonify
from flask_session import Session
import matplotlib.pyplot as plt
from environment import *

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'J$n@M,D(25)'
Session(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game', methods=['POST', 'GET'])
def game():
    if request.method=="GET":
        session['board']=Board(random_password())
        return render_template('game.html', **colors)
    else:
        if "answer" in request.form:
            answer=[number_to_color[c] for c in tolist(session['board'].pwd)]
            return jsonify({'a_pin1':answer[0],'a_pin2':answer[1],'a_pin3':answer[2],'a_pin4':answer[3]})
        else:
            pin1, pin2, pin3, pin4=request.form.get("pin1"), request.form.get("pin2"), request.form.get("pin3"), request.form.get("pin4")
            combination=todict(tuple([color_to_number[c] for c in (pin1, pin2, pin3, pin4)]))
            session['board'].append(combination)
            line,w,r,tries=session['board'].lines[-1],session['board'].reds[-1],session['board'].whites[-1],session['board'].tries
            if r==4:
                return jsonify({'correct':True, 'tries':str(tries)})
            else:
                return jsonify({'correct':False, 'w':w, 'r':r, 'tries':str(tries), 'old_pin1':pin1, 'old_pin2':pin2, 'old_pin3':pin3, 'old_pin4':pin4})

@app.route('/solver', methods=['POST', 'GET'])
def solver():
    if request.method=="GET":
        return render_template('solver.html', **colors)
    else:
        pwd=tuple([color_to_number[request.form.get("pin"+str(i))] for i in range(1,5)])
        board = Board(todict(pwd))
        gen = get_best_gen(database.get_contents("database"))
        url = "database/generation_"+str(gen)+"/net_0.csv"
        content = database.get_contents(url, ref="main")
        title, forget_list, input_list, output_list, memory_list = content.decoded_content.decode().split("\n")
        forget_gate, input_gate, output_gate, memory_gate = Gate.from_csv(forget_list, "sigmoid"), Gate.from_csv(input_list, "sigmoid"), Gate.from_csv(output_list, "sigmoid"), Gate.from_csv(memory_list, "tanh")
        ai = LSTM(forget_gate.input_size, forget_gate.output_size, gates=[forget_gate, input_gate, output_gate, memory_gate])
        results = play_game(ai, 15, 15, board, True)
        lines=[tuple(map(lambda x: number_to_color[x],tolist(l))) for l in results.lines]
        done = True
        if results.reds[-1]!=4:
            p = results.p
            if len(p)>1:
                done = False
            else:
                lines.append(tuple(map(lambda x: number_to_color[x],tolist(p[0]))))
                results.reds.append(4)
                results.whites.append(0)
                results.tries+=1
        return jsonify({'tries':results.tries, 'w':results.whites, 'r':results.reds, 'moves':lines, 'done':done})