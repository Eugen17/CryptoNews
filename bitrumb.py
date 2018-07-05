from config import BOT_TOKEN, BASE_URL_BITRUMB
from post import *
from binance import get_html_soup, is_exist_byurl
import telebot
from bot import bot


def get_first_references_bitrumb():
    references = []
    soup = get_html_soup(BASE_URL_BITRUMB)
    list_items = soup.find_all("h3", {"class": "entry-title"})
    for item in list_items[0:5]:
        if is_exist_byurl(get_article_url_bitrumb(item)):
            continue
        else:
            references.append(get_article_url_bitrumb(item))
    return references


def get_article_url_bitrumb(item):
    tag = item.find("a")
    info_source = tag.get("href")
    return info_source


def get_bitrumb_text_article(html):
    #soup = get_html_soup(html)
    text = []
    #news_header = soup.find("h3", {"class": "entry-title"})
    text.append({
        #'header': "*" + news_header.text.strip() + "*" + "\n",
        #'filling': " ",
        'url': html
    })
    return text[0]


def get_first_news_bitrumb():
    list_news = []
    list_urls = get_first_references_bitrumb();
    for item in list_urls:
        list_news.append(get_bitrumb_text_article(item))
    return list_news


def check_save_send_bitrumb(list_news):
    for item in list_news:
        hui = Post( url=item['url'])
        bot.send_message(CHAT,  hui.url, parse_mode='markdown')
        hui.save()
