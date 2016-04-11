# -*- coding:utf-8 -*-

from flask import Flask

from app import app

app.run(host='0.0.0.0',debug=True, port=5000)
