# -*- coding:utf-8 -*-
from flask import request
from flask.json import jsonify

from app import app
from app.Model import User, UserFriend
from app.databases import DBSession
import json


@app.route('/')
@app.route('/index')
def index():
    return "Hello,World"


@app.route('/users', methods=['GET'])
def get_users():
    session = DBSession()
    users = session.query(User).all()
    userjson = {}
    for user in users:
        task = user.__dict__
        task.pop('_sa_instance_state')
        userjson[user.id] = task
    session.close()
    return json.dumps(userjson, encoding='utf-8')


@app.route('/users/dologin', methods=['POST'])
def dologin():
    session = DBSession()
    userjson = request.json
    username = userjson.get('username')
    userpassword = userjson.get('password')
    user = session.query(User).filter(User.username == username, User.password == userpassword).first()
    session.close()
    if user is None:
        message = {'message': False}
        return json.dumps(message)
    else:
        message = {'message': True}
        return json.dumps(message)


@app.route('/users/doregister', methods=['POST'])
def doregister():
    session = DBSession()
    userjson = request.json
    username = userjson.get('username')
    password = userjson.get('password')
    sex = userjson.get('sex')
    photo = userjson.get('photo')
    adduser = User(username, password, sex, photo)
    user = session.query(User).filter(User.username == username)
    if user is not None:
        message = {"message": False}
        session.close()
        return json.dumps(message)
    else:
        session.add(adduser)
        session.commit()
        session.close()
        message = {"message": True}
        return json.dumps(message)


@app.route('/users/addfriend', methods=['POST'])
def doaddfriends():
    session = DBSession()
    friendsjson = request.json
    user_id = friendsjson.get('user_id')
    friends_id = friendsjson.get('friends_id')
    friend = session.query(UserFriend).filter(UserFriend.user_id == user_id, UserFriend.friend_id == friends_id).first()
    if friend is None:
        user = session.query(User).filter(User.id == user_id).one()
        friend = session.query(User).filter(User.id == friends_id).one()
        session.close()
        friend.registerObserver(user)
        message = {'message': True}
        return json.dumps(message)
    else:
        message = {'message': False}
        return json.dumps(message)


@app.route('/users/removefriend', methods=['POST'])
def doremovefriends():
    session = DBSession()
    friendsjson = request.json
    user_id = friendsjson.get('user_id')
    friends_id = friendsjson.get('friends_id')
    friend = session.query(UserFriend).filter(UserFriend.user_id == user_id, UserFriend.friend_id == friends_id).first()
    if friend is not None:
        friends = session.query(User).filter(User.id == friends_id).one()
        users = session.query(User).filter(User.id == user_id).one()
        session.close()
        friends.removeObserver(users)
        message = {'message': True}
        return json.dumps(message)
    else:
        message = {'message': False}
        return json.dumps(message)
