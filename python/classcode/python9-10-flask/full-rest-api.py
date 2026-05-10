from flask import Flask,request
from utils import user_validator,app_log
import datetime

app = Flask(__name__)


@app.before_request
def before_request_func():
    app_log(f'{request.method} {request.path} at {datetime.datetime.now()}')


users = [
    {'id':1,'username':'noam','password':'1234','email':'noam@ops.com','age':50},
    {'id':2,'username':'shirley','password':'12344','email':'shirley@dev.com','age':50},
    {'id':3,'username':'guy','password':'123444','email':'guy@sec.com','age':100}
]


# GET all users
@app.get('/users')
def get_users():
    # print(f'GET /users {datetime.datetime.now()}')
    return users

# Get user by id
@app.get('/users/<int:id>')
def get_user(id):
    for user in users:
        if user['id']==id:
            return user # type is dict

# delete by id
@app.delete('/users/<int:id>')
def delete_user(id):
    for user in users:
        if user['id'] == id:
            users.remove(user)
    return {'status':'success','msg':f'user {id} deleted'},200 # response str-dict-list , status code


# delete all
@app.delete('/users')
def delete_all():
    users.clear()
    return {'status': 'success'}


# add new user to the users list (DB)
# -> recieve user json V
# -> validate the items 'keys' 
# -> add to users list and returns 201 status code

# add user
@app.post('/users')
def add_user():
    data = request.get_json()
    if user_validator(data):
        data['id']= users[-1]['id']+1
        users.append(data)
        return {'status':'success'},201
    else:
        app_log(f'{request.url} bad request -- missing keys in json receieved jsos = {data}')
        return {'status':'error','msg':'bad request -- missing keys in json'},400
    # print(f'this is the data form the request {data}')
    

# PUT - update/replace entire user by id
@app.put('/users/<int:id>')
def update_user(id):
    data = request.get_json()
    if not user_validator(data):
        return {'status':'error','msg':'bad request -- missing keys in json'},400
    for i, user in enumerate(users):
        if user['id'] == id:
            data['id'] = id
            users[i] = data
            return {'status':'success','msg':f'user {id} updated'},200
    return {'status':'error','msg':f'user {id} not found'},404


# PATCH - partial update user by id
@app.patch('/users/<int:id>')
def patch_user(id):
    data = request.get_json()
    for user in users:
        if user['id'] == id:
            for key, value in data.items():
                if key != 'id':
                    user[key] = value
            return {'status':'success','msg':f'user {id} patched','user':user},200
    return {'status':'error','msg':f'user {id} not found'},404


app.run(port=5005, debug=True) #port-5000 