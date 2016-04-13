#-*- coding:utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

engine = create_engine('mysql+mysqldb://root:940304@localhost:3305/simpleweibo?charset=utf8')
DBSession = sessionmaker(bind=engine)