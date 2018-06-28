from mongoengine import *


connect('trades', alias='default')


class Post(Document):
    header = StringField()
    filling = StringField()
    url = StringField()


class UpPost(Document):
    header = StringField()
    filling = StringField()
    url = StringField()
    urlup = StringField()


 
