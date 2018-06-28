from mongoengine import *
import telebot




connect('trades', alias='default')


class Post(Document):
    header = StringField()
    filling = StringField()
    url = StringField()
    news_id = IntField()
