from flask import Flask, request

app = Flask(__name__)

users_list = ['elad', 'guy', 'sahar', 'aviel', 'eitan', 'elia']


# app.method /resource
@app.get('/users')
def users():
    return users_list


@app.get('/')
def index():
    return "homepage"


@app.get('/greet/<name>')
def greet(name):
    return f"welcome {name}"


# http://elia:8000/add/hodi/222
@app.get('/add/<string:a>/<int:b>')
def spadd(a, b):
    return f'{a} -- {b}'


# http://elia:8000/add/1999/222
@app.get('/add/<int:a>/<int:b>')
def add(a, b):
    return f" {a} + {b} = {a + b}"


@app.get('/ip')
def ip():
    print(request.headers)
    return f'{request}'


app.run(port=8000)
