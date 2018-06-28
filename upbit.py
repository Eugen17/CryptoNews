from config import BOT_TOKEN, BASE_URL_UPBIT, CHAT
from post import *
from binance import get_html_soup, get_filling_article
import telebot
import json
from bot import bot


def get_first_references_upbit():
    references = []
    i = 399
    while True:
        while not is_exist_byurl(BASE_URL_UPBIT + str(i)):
            if isvalid(BASE_URL_UPBIT + str(i)):
                references.append(BASE_URL_UPBIT + str(i))
                i = i + 1
            else:
                return references
        i = i + 1
    return references


def is_exist_byurl(filling):
    try:  # Хуйня нагружает проц. Никто так не делает, нужен "иф"
        UpPost.objects.get(url=filling)
        return True
    except:
        return False


def isvalid(url):
    soup = json.loads(str(get_html_soup(url)))
    try:
        p = soup["data"]
        return True
    except:
        return False


def get_upbit_text_article(html):
    soup = json.loads(str(get_html_soup(html)))
    text = []
    news_header = soup['data']['title']
    paragraphs = soup['data']['body']
    text.append({
        'header': "*" + news_header + "*" + "\n",
        'filling': str(paragraphs) + "\n",
        'url': html,
        'urlup': 'https://upbit.com/service_center/notice?id=' + get_filling_article(html[-3:])
    })
    return text[0]


def get_first_news_upbit():
    list_news = []
    list_urls = get_first_references_upbit();
    for item in list_urls:
        list_news.append(get_upbit_text_article(item))
    return list_news


def check_save_send_upbit(list_news):
    for item in list_news:
        hui = UpPost(header=item['header'], filling=item['filling'], url=item['url'], urlup=item["urlup"])
        hui.save()
        bot.send_message('-1001303379218', hui.header, parse_mode="markdown")
        bot.send_message('-1001303379218', hui.filling)
        bot.send_message('-1001303379218', hui.urlup)


# почему этв хуйня не работает в посте
# hui.save()


def main():
    check_save_send_upbit(get_first_news_upbit())


if __name__ == '__main__':
    main()
