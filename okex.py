from config import BOT_TOKEN, HEADERS, BASE_URL_OKEX, CHAT
from post import *
from binance import get_html_soup, is_exist_byurl, get_filling_article
import telebot
from bot import bot


def get_first_references_okex():
    references = []
    soup = get_html_soup("https://support.okex.com/hc/en-us/sections/115000447632-New-Token")
    list_items = soup.find_all("a", {"class": "article-list-link"})
    for item in list_items[0:5]:
        if is_exist_byurl(BASE_URL_OKEX + get_article_url_okex(item)):
            continue
        else:
            references.append(BASE_URL_OKEX + get_article_url_okex(item))
    return references


def get_article_url_okex(tag):
    info_source = tag.get("href")
    return info_source


def get_okex_text_article(html):
    soup = get_html_soup(html)
    text = []
    news_header = soup.find("h1", {"class": "article-title"})
    paragraphs = soup.find("div", {"class": "article-body"})
    list_important_paragraphs = []
    news_paragraphs = paragraphs.find_all('p')
    for paragraph in news_paragraphs:
        if paragraph.text.find("You may find more information about the token(s) here") !=(-1):
            break
        else:
            list_important_paragraphs.append("\n" + paragraph.text)
    text.append({
        'header': "*" + news_header.text.strip() + "*" + "\n",
        'filling': get_filling_article(list_important_paragraphs) + "\n",
        'url': html
    })
    return text[0]


def get_first_news_okex():
    list_news = []
    list_urls = get_first_references_okex();
    for item in list_urls:
        list_news.append(get_okex_text_article(item))
    return list_news


def check_save_send_okex(list_news):
    for item in list_news:
        hui = Post(header=item['header'], filling=item['filling'], url=item['url'])
        bot.send_message("-1001303379218", hui.header + hui.filling + hui.url, parse_mode='markdown')
        hui.save()
