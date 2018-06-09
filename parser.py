import requests
import soup as soup
from bs4 import BeautifulSoup
from config import BOT_TOKEN, HEADERS, BASE_URL


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
			list_important_paragraphs.append(paragraph.text)
	text.append({
		'header': news_header.text,
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
    info_source = BASE_URL + reference
    return info_source

def main():
	print(get_text_binance_article("https://support.binance.com/hc/en-us/articles/360004692771-Binance-Supports-ONT-Mainnet-Swap-and-Adds-ONT-USDT-Trading-Pair-")['filling'])
	print(get_first_5_references())


if __name__ == '__main__':
	main()



