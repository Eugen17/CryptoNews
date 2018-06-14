import requests
import soup as soup
from bs4 import BeautifulSoup
from config import BOT_TOKEN, HEADERS, BASE_URL_OKEX, CHAT
from post import *
from binance import get_html_soup,is_exist_byfilling
import telebot


bot = telebot.TeleBot(BOT_TOKEN)

def get_first_references_okex():
	references = []
	soup = get_html_soup(BASE_URL_OKEX+"/hc/en-us/sections/115000437971-Cryptocurrency-Intro")
	list_items = soup.find_all("a", {"class": "article-list-link"})
	for item in list_items[0:5]:
		if (is_exist_byurl(BASE_URL_OKEX+get_article_url_okex(item))):
			continue
		else:
			references.append(BASE_URL_OKEX+get_article_url_okex(item))
	return references


def get_article_url_okex(tag):
	info_source = tag.get("href")
	return info_source	
#soup.find('iframe').get('src')

def get_okex_text_article(html):
	soup = get_html_soup(html)
	text = []
	news_header = soup.find("h1", {"class": "article-title"})
	paragraphs = soup.find("div", {"class": "article-body"})
	news_paragraphs = paragraphs.find_all('div')
	list_important_paragraphs = []
	if (len(news_paragraphs) == 0):
		news_paragraphs = paragraphs.find_all('p')
		if (len(news_paragraphs)>10):
			for paragraph in news_paragraphs[-14:-6]:
				list_important_paragraphs.append("\n"+paragraph.text)
		else:		
			for paragraph in news_paragraphs[1:-2]:
				list_important_paragraphs.append("\n"+paragraph.text)
	else:
		for paragraph in news_paragraphs[-27:-8]:
				list_important_paragraphs.append("\n"+paragraph.text)		
	
	
	text.append({
		'header': "*" + news_header.text.strip() + "*"+"\n",
		'filling': get_filling_article(list_important_paragraphs)+"\n",
		'url':html
		})
	return text[0]


def get_filling_article(list_news):
	maintext=''
	for item in list_news:
		maintext+=item
	return maintext	


def get_first_news_okex():
	list_news = []
	list_urls = get_first_references_okex();
	for item in list_urls:
		list_news.append(get_okex_text_article(item))
	return list_news	


def is_exist_byurl(url1):
    	try:
    		post = Post.objects.get(url = url1)
    		return True
    	except:
    		return False	


def check_save_send_okex (list_news):
	bot = telebot.TeleBot(BOT_TOKEN)

	for item in list_news:
		hui = Post(header = item['header'], filling = item['filling'], url = item['url'])
		bot.send_message(CHAT, hui.header+hui.filling+ hui.url,parse_mode='markdown')
		#почему этв хуйня не работает в посте
		hui.save()


def main():
	check_save_send_okex(get_first_news_okex())


if __name__ == '__main__':
	main()