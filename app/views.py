# -*- coding:utf-8 -*-
import base64
import os
import time
from datetime import datetime

from flask import request, session, url_for, send_from_directory, render_template

from app import app
from app.Model import User, UserFriend, Blog, Answer, BlogImage
from app.databases import DBSession
import json

UPLOAD_FOLDER = '/image/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/<path:path>')
def send_image(path):
    return send_from_directory('static/', path)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/users/getuserinfo/<int:user_id>', methods=['GET'])
def get_users(user_id):
    dbsession = DBSession()
    user = dbsession.query(User).filter(User.id == user_id).one()
    task = user.__dict__
    task.pop('_sa_instance_state')
    task.pop('password')
    return json.dumps(task)


@app.route('/users/dologin', methods=['POST'])
def dologin():
    dbsession = DBSession()
    userjson = request.json
    username = userjson.get('username')
    userpassword = userjson.get('password')
    user = dbsession.query(User).filter(User.username == username, User.password == userpassword).first()
    dbsession.close()
    if user is None:
        message = {'message': False}
        return json.dumps(message)
    else:
        message = {'message': True, 'user_id': user.id}
        return json.dumps(message)


@app.route('/users/dologout', methods=['POST'])
def dologout():
    userjson = request.json
    username = userjson.get('username')
    if username in session:
        session.pop('user', None)
    message = {'message': True}
    return json.dumps(message)


@app.route('/users/doregister', methods=['POST'])
def doregister():
    dbsession = DBSession()
    userjson = request.json
    username = userjson.get('username')
    password = userjson.get('password')
    sex = userjson.get('sex')
    photo = 'http://192.168.1.112:5000/2.png'
    print sex
    adduser = User(username, password, sex, photo)
    user = dbsession.query(User).filter(User.username == username).first()
    print user
    if user is not None:
        message = {"message": False}
        dbsession.close()
        return json.dumps(message)
    else:
        dbsession.add(adduser)
        dbsession.commit()
        dbsession.close()
        message = {"message": True}
        return json.dumps(message)


@app.route('/users/addfriend', methods=['POST'])
def doaddfriends():
    dbsession = DBSession()
    friendsjson = request.json
    user_id = friendsjson.get('user_id')
    friends_id = friendsjson.get('friends_id')
    friend = dbsession.query(UserFriend).filter(UserFriend.user_id == user_id,
                                                UserFriend.friend_id == friends_id).first()
    if friend is None:
        user = dbsession.query(User).filter(User.id == user_id).one()
        friend = dbsession.query(User).filter(User.id == friends_id).one()
        dbsession.close()
        user.registerObserver(friend)
        message = {'message': True}
        return json.dumps(message)
    else:
        message = {'message': False}
        return json.dumps(message)


@app.route('/users/removefriend', methods=['POST'])
def doremovefriends():
    dbsession = DBSession()
    friendsjson = request.json
    user_id = friendsjson.get('user_id')
    friends_id = friendsjson.get('friends_id')
    friend = dbsession.query(UserFriend).filter(UserFriend.user_id == user_id,
                                                UserFriend.friend_id == friends_id).first()
    if friend is not None:
        friends = dbsession.query(User).filter(User.id == friends_id).one()
        users = dbsession.query(User).filter(User.id == user_id).one()
        dbsession.close()
        users.removeObserver(friends)
        message = {'message': True}
        return json.dumps(message)
    else:
        message = {'message': False}
        return json.dumps(message)


@app.route('/users/writeblog', methods=['POST'])
def writeblogs():
    dbsession = DBSession()
    writeblogs = request.json
    user_id = writeblogs.get('user_id')
    content = writeblogs.get('content')
    blog_imagejson = writeblogs.get('blog_image')
    fromBlog_id = 1
    fromUser_id = user_id
    fowardNum = 0
    issueTime = datetime.now().date()
    blog = Blog(user_id, content, fromBlog_id, fromUser_id, fowardNum, issueTime)
    dbsession.add(blog)
    dbsession.flush()
    if blog_imagejson is not '':
        imagedata = base64.b64decode(blog_imagejson)
        path = os.path.join(os.path.dirname(__file__), os.path.pardir)
        pathpartent = os.path.abspath(path) + '/static/' + 'blog_' + str(blog.id)
        image = open(pathpartent + '.png', 'wb')
        image.write(imagedata)
        image.close()
        blogimage = BlogImage('http://192.168.1.112:5000' + '/static/' + 'blog_' + str(blog.id) + '.png', blog.id)
        dbsession.add(blogimage)
    dbsession.commit()
    dbsession.close()
    message = {'message': True}
    return json.dumps(message)


@app.route('/users/getallblog', methods=['GET'])
def getallblog():
    dbSession = DBSession()
    blogs = dbSession.query(Blog).all()
    blogjson = []
    for blog in blogs:
        userid = blog.user_id
        user = dbSession.query(User).filter(User.id == userid).one()
        username = user.username
        task = blog.__dict__
        task.pop('_sa_instance_state')
        d = task.get('issueTime')
        t = d.strftime("%Y-%m-%d")
        task['issueTime'] = t
        friend_id = blog.user_id
        friend = dbSession.query(User).filter(User.id == friend_id).one()
        friend_name = friend.username
        task['user_name'] = friend_name
        task['user_photo'] = friend.photo
        if blog.fromBlog_id > 1:
            forward_blog = dbSession.query(Blog).filter(Blog.id == blog.fromBlog_id).one()
            task['forward_content'] = forward_blog.content
        blogjson.append(task)
    dbSession.close()
    return json.dumps(blogjson)


@app.route('/users/getfriendblogs/<int:user_id>', methods=['GET'])
def getfriendblog(user_id):
    dbsession = DBSession()
    user = dbsession.query(User).filter(User.id == user_id).one()
    bloges = user.display()
    print bloges
    blogjson = []
    for blogs in bloges:
        for blog in blogs:
            task = blog.__dict__
            task.pop('_sa_instance_state')
            d = task.get('issueTime')
            t = d.strftime("%Y-%m-%d")
            task['issueTime'] = t
            friend_id = blog.user_id
            friend = dbsession.query(User).filter(User.id == friend_id).one()
            friend_name = friend.username
            task['user_name'] = friend_name
            task['user_photo'] = friend.photo
            if blog.fromBlog_id > 1:
                forward_blog = dbsession.query(Blog).filter(Blog.id == blog.fromBlog_id).one()
                task['forward_content'] = forward_blog.content
            blogjson.append(task)
    dbsession.close()
    return json.dumps(blogjson)


@app.route('/users/getblogs/<int:blog_id>', methods=['GET'])
def getblogbyid(blog_id):
    dbsession = DBSession()
    blog = dbsession.query(Blog).filter(Blog.id == blog_id).one()
    user = dbsession.query(User).filter(User.id == blog.user_id).one()
    print blog
    task = blog.__dict__
    task.pop('_sa_instance_state')
    d = task.get('issueTime')
    t = d.strftime("%Y-%m-%d")
    task['issueTime'] = t
    task['user_name'] = user.username
    task['user_photo'] = user.photo
    if blog.fromBlog_id > 1:
        forward_blog = dbsession.query(Blog).filter(Blog.id == blog.fromBlog_id).one()
        task['forward_content'] = forward_blog.content
    dbsession.close()
    return json.dumps(task)


@app.route('/user/fowardblog', methods=['POST'])
def fowardblog():
    dbsession = DBSession()
    writeblogs = request.json
    user_id = writeblogs.get('user_id')
    content = writeblogs.get('content')
    fromBlog_id = writeblogs.get('fromBlog_id')
    fromUser_id = writeblogs.get('fromUser_id')
    fowardNum = 0
    issueTime = datetime.now().date()
    blog = Blog(user_id, content, fromBlog_id, fromUser_id, fowardNum, issueTime)
    dbsession.add(blog)
    dbsession.commit()
    dbsession.close()
    message = {'message': True}
    return json.dumps(message)


@app.route('/user/addanswer', methods=['POST'])
def addanswer():
    dbSession = DBSession()
    addanswerjson = request.json
    fromUser_id = addanswerjson.get('fromUser_id')
    toUser_id = 1
    blog_id = addanswerjson.get('blog_id')
    content = addanswerjson.get('content')
    resTime = datetime.now().date()
    if content is not '' and not None:
        answer = Answer(fromUser_id, toUser_id, blog_id, content, resTime)
        dbSession.add(answer)
        dbSession.commit()
        dbSession.close()
        message = {'message': True}
        return json.dumps(message)
    else:
        message = {'message': False}
        return json.dumps(message)


@app.route('/user/getanswer/<int:blog_id>', methods=['GET'])
def getanswer(blog_id):
    dbSession = DBSession()
    answers = dbSession.query(Answer).filter(Answer.bolg_id == blog_id).all()
    ansersjson = []
    for answer in answers:
        task = answer.__dict__
        task.pop('_sa_instance_state')
        d = task.get('resTime')
        t = d.strftime("%Y-%m-%d")
        task['resTime'] = t
        fromUser = dbSession.query(User).filter(User.id == answer.fromUser_id).first()
        toUser = dbSession.query(User).filter(User.id == answer.toUser_id).first()

        if toUser.id > 1:
            task['toUsername'] = toUser.username
        task['from_User_name'] = fromUser.username
        ansersjson.append(task)
    return json.dumps(ansersjson)


@app.route('/user/uploadphoto', methods=['POST'])
def upload_file():
    imagejson = request.json
    user_id = imagejson.get('user_id')
    user_photo = imagejson.get('user_photo')
    dbsession = DBSession()
    photodata = base64.b64decode(user_photo)
    path = os.path.join(os.path.dirname(__file__), os.path.pardir)
    pathpartent = os.path.abspath(path) + '/static/'
    image = open(pathpartent + str(user_id) + '.png', 'wb')
    image.write(photodata)
    image.close()
    dbsession = DBSession()
    dbsession.query(User).filter(User.id == user_id).update(
        {'photo': 'http://192.168.1.112:5000/static/' + str(user_id) + '.png'})
    dbsession.commit()
    dbsession.close()
    message = {"message": True}
    return json.dumps(message)


@app.route('/user/getblogimage/<int:blog_id>', methods=['GET'])
def getblogimage(blog_id):
    dbsession = DBSession()
    blogimages = dbsession.query(BlogImage).filter(BlogImage.blog_id == blog_id).all()
    blogimagejson = []
    for blogimage in blogimages:
        task = blogimage.__dict__
        task.pop('_sa_instance_state')
        blogimagejson.append(task)
    return json.dumps(blogimagejson)


@app.route('/users/getfriends/<int:user_id>',methods=['GET'])
def getuserfriend(user_id):
    dbsession = DBSession()
    userfriends = dbsession.query(UserFriend).filter(UserFriend.user_id == user_id).all()
    userjson = []
    for userfrined in userfriends:
        friend_id = userfrined.friend_id
        user = dbsession.query(User).filter(User.id == friend_id).first()
        task = user.__dict__
        task.pop('_sa_instance_state')
        task.pop('password')
        userjson.append(task)
    return json.dumps(userjson)

app.secret_key = '\xcd\x1d\x07*\x82\xfe\xeeG\x93\x10\x8c~l\x1d\xb0\xa3\xce\xf2Nf\xc1[\x8e\xd4'
