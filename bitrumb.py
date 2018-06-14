import requests
import soup as soup
from bs4 import BeautifulSoup
from config import BOT_TOKEN, HEADERS, BASE_URL_BITRUMB, CHAT
from post import *
from binance import get_html_soup,is_exist_byfilling
import telebot


bot = telebot.TeleBot(BOT_TOKEN)

def get_first_5_references_bitrumb():
	references = []
	soup = get_html_soup(BASE_URL_BITRUMB)
	list_items = soup.find_all("h3", {"class": "entry-title"})
	for item in list_items[0:5]:
		references.append(get_article_url_bitrumb(item))
	return references


def get_article_url_bitrumb(item):
	tag = item.find("a")
	info_source = tag.get("href")
	return info_source	
#soup.find('iframe').get('src')

def get_bitrumb_text_article(html):
	soup = get_html_soup(html)
	text = []
	news_header = soup.find("h3", {"class": "entry-title"})
	
	# print (news_header)
	# pages = soup_doc.find_all("div", {"class": "ndfHFb-c4YZDc-cYSp0e-DARUcf"})
	# print(len(pages))
	# news_paragraphs = pages[3].find_all('p')
	# list_important_paragraphs = []
	# for paragraph in news_paragraphs[1:]:
	# 	if (paragraph.text == "나. 주요 스펙"):
	# 		break
	# 	else:
	# 		list_important_paragraphs.append("\n"+paragraph.text+"\n")
	text.append({
		'header': "*" + news_header.text.strip() + "*"+"\n",
		'filling': " ",
		'url':html
		})
	return text[0]


def get_filling_article(list):
	maintext=''
	for item in list:
		maintext+=item
	return maintext	


def get_first_5news_bitrumb():
	list_news = []
	list_urls = get_first_5_references_bitrumb();
	for item in list_urls:
		list_news.append(get_bitrumb_text_article(item))
	return list_news	


def is_exist_byurl(url1):
    	try:
    		post = Post.objects.get(url = url1)
    		return True
    	except:
    		return False	


def check_save_send_bitrumb (list_news):
	bot = telebot.TeleBot(BOT_TOKEN)

	for item in list_news:
		if (is_exist_byurl(item['url'])):
			break
		else:
			hui = Post(header = item['header'], filling = item['filling'], url = item['url'])
			bot.send_message("-1001303379218", hui.header+hui.filling+ hui.url,parse_mode='markdown')
			#почему этв хуйня не работает в посте
			hui.save()


def main():
	check_save_send_bitrumb (get_first_5news_bitrumb())


if __name__ == '__main__':
	main()