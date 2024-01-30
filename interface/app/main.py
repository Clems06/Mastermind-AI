from flask import Flask, render_template, request, session, jsonify
from flask_session import Session
from environment import *
from github import Github
import matplotlib.pyplot as plt

token="ghp"+"_kAPYTVnLUCao5zAupm0HTN3rucmPVL3i19vB"
g = Github(token)
database=g.get_repo("Clems06/Mastermind-AI")

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
        session['board']=Board("Game", random_password())
        return render_template('game.html', **colors)
    else:
        if "answer" in request.form:
            answer=[number_to_color[c] for c in tolist(session['board'].pwd)]
            return jsonify({'a_pin1':answer[0],'a_pin2':answer[1],'a_pin3':answer[2],'a_pin4':answer[3]})
        else:
            pin1, pin2, pin3, pin4=request.form.get("pin1"), request.form.get("pin2"), request.form.get("pin3"), request.form.get("pin4")
            combination=todict(tuple([color_to_number[c] for c in (pin1, pin2, pin3, pin4)]))
            session['board'].append(combination)
            line=session['board'].lines[-1]
            if line.r==4:
                return jsonify({'correct':True, 'tries':str(len(session['board'].lines))})
            else:
                return jsonify({'correct':False, 'w':line.w, 'r':line.r, 'tries':str(len(session['board'].lines)), 'old_pin1':pin1, 'old_pin2':pin2, 'old_pin3':pin3, 'old_pin4':pin4})

@app.route('/ai')
def ai():
    content=database.get_contents("database/general.csv", ref="main").decoded_content.decode()
    current=content.split('\n')[1].split(',')
    current[0]=current[0][2:]
    current[1]=current[1].split('|')[::-1]
    current[3]=[[[number_to_color[int(i)] for i in j] for j in c.split(';')] for c in current[3].split('|')][::-1]
    glob=[]
    for line in content.split('\n')[2:]:
        if line!='':
            div=line.split(',')
            glob.append([div[0],div[1],div[2],[[number_to_color[int(i)] for i in j] for j in div[3].split(';')]])
    return render_template('ai.html', current=current, glob=glob)