from mongoengine import *
import telebot



CHAT = '389904727'
connect('trades', alias='default')


class Post(Document):
    header = StringField()
    filling = StringField()
    url = StringField()
    news_id = IntField()

    #def send(self,bot):
    #	bot.send_message(chat_id = CHAT,
     #                text = self.filling
      #            	 )
    