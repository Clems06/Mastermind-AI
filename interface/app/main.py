from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'J$n@M,D(25)'

colors={'red':"#D90404", 'blue':"#05C7F2", 'green':"#078C03", 'yellow':"#F2B705", 'orange':"#F25C05", 'pink':"#F288A4", 'violet':"#4A2ABF",'grey':"#606B73"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game', methods=['POST', 'GET'])
def game():
    return render_template('game.html', **colors)

@app.route('/ai')
def ai():
    return render_template('ai.html')