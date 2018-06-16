from mongoengine import *

CHAT = '389904727'
connect('trades', alias='default')


class Post(Document):
    header = StringField()
    filling = StringField()
    url = StringField()

    def send(self,bot):
        bot.send_message(chat_id=CHAT,
                     text=self.filling
                     )
    

class UpPost(Document):
    header = StringField()
    filling = StringField()
    url = StringField()
    urlup = StringField()


 
