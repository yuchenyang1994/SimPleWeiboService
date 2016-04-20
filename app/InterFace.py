# -*- coding:utf-8 -*-
from abc import ABCMeta, abstractmethod


class Subject(object):

    def registerObserver(self, Observer):
        pass

    def removeObserver(self, Observer):
        pass

    def notyfiObserver(self,Blog):
        pass


class Observer(object):

    def updateblog(self,Blog):
        pass

class DisplayElement(object):

    def display(self):
        pass