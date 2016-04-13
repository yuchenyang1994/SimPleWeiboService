# -*- coding:utf-8 -*-
from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship

from app.InterFace import Subject, Observer, DisplayElement
from databases import Base, DBSession


class User(Base, Subject, Observer, DisplayElement):
    __tablename__ = 'User'
    id = Column(Integer(), primary_key=True)
    username = Column(String(50))
    password = Column(String(50))
    sex = Column(String(50))
    photo = Column(String(255))
    friends = relationship('UserFriend')

    def __init__(self, username, password, sex, photo):
        self.username = username
        self.password = password
        self.sex = sex
        self.photo = photo
        self.Observers = []
        self.Change = True

    def registerObserver(self, Observer):
        session = DBSession()
        friend_id = Observer.id
        friend = UserFriend(friend_id, self.id)
        session.add(friend)
        session.commit()
        session.close()
        return

    def removeObserver(self, Observer):
        session = DBSession()
        friend_id = Observer.id
        friend = session.query(UserFriend).filter(UserFriend.user_id == self.id, UserFriend.friend_id == friend_id).first()
        session.delete(friend)
        session.commit()
        session.close()
        return

    # def notyfiObserver(self, Blog):
    #     session = DBSession()
    #     friends = session.query(UserFriend).filter(UserFriend.user_id == self.id).all()
    #     for i in friends:
    #         friendsobj = session.query(User).filter(User.id == i.friend_id).all()
    #         self.Observers = friendsobj
    #     for item in self.Observers:
    #         item.update(Blog)
    #     session.close()
    #     return

    def update(self, Blog):
        if self.Change:
            session = DBSession()
            session.add(Blog)
            session.commit()
            session.close()
            self.Change = False
        return

    def display(self):
        session = DBSession()
        userfriends = session.query(UserFriend).filter(UserFriend.user_id == self.id).all()
        blogs = None
        for item in userfriends:
            friends_id = item.friend_id
            blogs = session.query(Blog).filter(Blog.user_id == friends_id).all()
        session.close()
        return blogs

    # def setChange(self, Blog):
    #     self.Change = True
    #     self.update(Blog)
    #     return


class UserFriend(Base):
    __tablename__ = 'UserFriend'
    id = Column(Integer(), primary_key=True)
    friend_id = Column(Integer())
    user_id = Column(Integer(), ForeignKey('User.id'))

    def __init__(self, friend_id, user_id):
        self.friend_id = friend_id
        self.user_id = user_id


class Blog(Base):
    __tablename__ = 'Blog'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    content = Column(String(255))
    fromBlog_id = Column(Integer())
    fromUser_id = Column(Integer())
    fowardNum = Column(Integer())
    issueTime = Column(DateTime)

    def __init__(self, user_id, content, fromBlog_id, fromUser_id, fowardNum, issueTime):
        self.user_id = user_id
        self.content = content
        self.fromBlog_id = fromBlog_id
        self.fromUser_id = fromUser_id
        self.fowardNum = fowardNum
        self.issueTime = issueTime


class BlogImage(Base):
    __tablename__ = 'BlogImage'
    id = Column(Integer(), primary_key=True)
    blog_image = Column(String(255))
    blog_id = Column(Integer(), ForeignKey('Blog.id'))

    def __init__(self, blog_image, blog_id):
        self.blog_id = blog_id
        self.blog_image = blog_image


class Answer(Base):
    __tablename__ = 'Answer'
    id = Column(Integer(), primary_key=True)
    fromUser_id = Column(Integer(), ForeignKey('User.id'))
    toUser_id = Column(Integer(), ForeignKey('User.id'))
    blog_id = Column(Integer(), ForeignKey('Blog.id'))
    content = Column(String(50))
    resTime = Column(DateTime)

    def __init__(self, fromUser_id, toUser_id, blog_id, content, resTime):
        self.fromUser_id = fromUser_id
        self.toUser_id = toUser_id
        self.blog_id = blog_id
        self.content = content
        self.resTime = resTime
