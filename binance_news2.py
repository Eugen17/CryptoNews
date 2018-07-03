from config import CHAT
from post import *
from binance import get_html_soup, is_exist_byurl, get_filling_article, get_article_url_binance
import telebot
from bot import bot


def get_text_binance_article(html):
    soup = get_html_soup(html)
    text = []
    news_header = soup.find("h1", {"class": "article-title"})
    news_filling = soup.find("div", {"class": "article-body"})
    news_paragraphs = news_filling.find_all('p')
    list_important_paragraphs = []
    for paragraph in news_paragraphs[1:]:
        if paragraph.text == "Binance Team":
            break
        else:
            list_important_paragraphs.append("\n" + paragraph.text + "\n")
    text.append({
        'header': "*" + news_header.text.strip() + "*",
        'filling': get_filling_article(list_important_paragraphs),
        'url': html
    })
    return text[0]


def get_first_references_binance2():
    references = []
    soup = get_html_soup("https://support.binance.com/hc/en-us/sections/115000202591-Latest-News")  # Я бы вынес линк
    list_items = soup.find_all("a", {"class": "article-list-link"})
    for item in list_items[0:5]:
        if is_exist_byurl(get_article_url_binance(item)):
            continue
        else:
            references.append(get_article_url_binance(item))
    return references


def get_first_news_binance2():
    list_news = []
    list_urls = get_first_references_binance2()
    for item in list_urls:
        list_news.append(get_text_binance_article(item))
    return list_news


def check_save_send_binance2(list_news):
    for item in list_news:
        hui = Post(header=item['header'], filling=item['filling'], url=item['url'])
        #bot.send_message(CHAT, hui.header, parse_mode='markdown')
        bot.send_message(CHAT, hui.url)
        hui.save()
