from flask import Flask, render_template, request
import sys
sys.path.append('...')
from environment import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'J$n@M,D(25)'

board=Board("Game")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game', methods=['POST', 'GET'])
def game():
    if request.method=="GET":
        board=Board("Game")
    else:
        pin1, pin2, pin3, pin4=request.form.get("pin1"), request.form.get("pin2"), request.form.get("pin3"), request.form.get("pin4")
        combination=todict(tuple([color_to_number[c] for c in (pin1, pin2, pin3, pin4)]))
        print(combination)
    return render_template('game.html', **colors, board=board, tries=str(1))

@app.route('/ai')
def ai():
    return render_template('ai.html')