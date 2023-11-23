from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'J$n@M,D(25)'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/ai')
def ai():
    return render_template('ai.html')