# -*- coding:utf-8 -*-

from flask import Flask, url_for

app = Flask(__name__,static_folder='../static/',template_folder='../templates',static_url_path='/static')
from app import views