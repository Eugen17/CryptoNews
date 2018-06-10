import requests
import soup as soup
from bs4 import BeautifulSoup
from config import BOT_TOKEN, HEADERS, BASE_URL_BINANCE
import telebot
CHAT = '389904727'

bot = telebot.TeleBot(BOT_TOKEN)
def get_html_soup(html):
    r = requests.get(html, headers=HEADERS)
    data_fromhtml = r.content
    soup = BeautifulSoup(data_fromhtml, "html.parser")
    return soup


def get_text_binance_article(html):
	soup = get_html_soup(html)
	text = []
	news_header = soup.find("h1", {"class": "article-title"})
	news_filling = soup.find("div", {"class": "article-body"})
	news_paragraphs =news_filling.find_all('p')
	list_important_paragraphs = []
	for paragraph in news_paragraphs[1:]:
		if (paragraph.text == "Details:"):
			break
		else:
			list_important_paragraphs.append("\n"+paragraph.text+"\n")
	text.append({
		'header': "*" + news_header.text.strip() + "*",
		'filling': list_important_paragraphs
		})
	return text[0]


def get_first_5_references():
	references = []
	soup = get_html_soup("https://support.binance.com/hc/en-us/sections/115000106672-New-Listings")
	list_items = soup.find_all("a", {"class": "article-list-link"})
	for item in list_items[0:5]:
		references.append(get_article_url(item))
	return references


def get_article_url(tag):
    reference = tag.get('href')
    info_source = BASE_URL_BINANCE + reference
    return info_source


def get_first_5news():
	list_news = []
	list_urls = get_first_5_references();
	for item in list_urls:
		list_news.append(get_text_binance_article(item))
	return list_news	


def main():
	print(get_text_binance_article("https://support.binance.com/hc/en-us/articles/360004692771-Binance-Supports-ONT-Mainnet-Swap-and-Adds-ONT-USDT-Trading-Pair-")['filling'][1])
	print(get_text_binance_article("https://support.binance.com/hc/en-us/articles/360004692771-Binance-Supports-ONT-Mainnet-Swap-and-Adds-ONT-USDT-Trading-Pair-")['filling'][2])
	bot.send_message(chat_id = CHAT,
                     text = (get_first_5news())[0]['header'] + get_first_5news()[0]['filling'][0]+get_first_5news()[0]['filling'][1],
                     parse_mode = 'markdown'
                     )
	print(get_first_5news())


if __name__ == '__main__':
	main()



