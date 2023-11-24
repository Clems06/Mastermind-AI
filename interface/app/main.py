from flask import Flask, render_template, request, session
from flask_session import Session
import flask_sijax
from environment import *

app = Flask(__name__)
app.config['SESSION_TYPE']='filesystem'
app.secret_key = 'J$n@M,D(25)'
Session(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game', methods=['POST', 'GET'])
def game():
    if request.method=="GET":
        session['board']=Board("Game")
    else:
        pin1, pin2, pin3, pin4=request.form.get("pin1"), request.form.get("pin2"), request.form.get("pin3"), request.form.get("pin4")
        combination=todict(tuple([color_to_number[c] for c in (pin1, pin2, pin3, pin4)]))
        print(combination)
        session['board'].append(combination)
        print(session['board'].lines)
    return render_template('game.html', **colors, board=session['board'])

@app.route('/ai')
def ai():
    return render_template('ai.html')