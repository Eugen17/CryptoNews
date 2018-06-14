import requests
from bs4 import BeautifulSoup
from config import HEADERS, BASE_URL_BINANCE, CHAT
from post import Post
from bot import bot


def get_html_soup(html):
    r = requests.get(html, headers=HEADERS)
    data_from_html = r.content
    soup = BeautifulSoup(data_from_html, "html.parser")
    return soup


def get_text_binance_article(html):
    soup = get_html_soup(html)
    text = []
    news_header = soup.find("h1", {"class": "article-title"})
    news_filling = soup.find("div", {"class": "article-body"})
    news_paragraphs = news_filling.find_all('p')
    list_important_paragraphs = []
    for paragraph in news_paragraphs[1:]:
        if paragraph.text == "Details:":
            break
        else:
            list_important_paragraphs.append("\n" + paragraph.text + "\n")
    text.append({
        'header': "*" + news_header.text.strip() + "*",
        'filling': get_filling_article(list_important_paragraphs),
        'url': html
        })
    return text[0]


def get_filling_article(list_):
    main_text = ''
    for item in list_:
        main_text += item
    return main_text


def get_first_5_references_binance():
    references = []
    soup = get_html_soup("https://support.binance.com/hc/en-us/sections/115000106672-New-Listings")  # Я бы вынес линк
    list_items = soup.find_all("a", {"class": "article-list-link"})
    for item in list_items[0:5]:
        references.append(get_article_url_binance(item))
    return references


def get_article_url_binance(tag):
    reference = tag.get('href')
    info_source = BASE_URL_BINANCE + reference
    return info_source


def get_first_5news_binance():
    list_news = []
    list_urls = get_first_5_references_binance()
    for item in list_urls:
        list_news.append(get_text_binance_article(item))
    return list_news


def is_exist_byfilling(filling):
    try:  # Хуйня нагружает проц. Никто так не делает, нужен "иф"
        Post.objects.get(header=filling)
        return True
    except:
        return False


def check_save_send_binance(list_news):
    for item in list_news:
        if is_exist_byfilling(item['header']):
            break
        else:
            hui = Post(header=item['header'], filling=item['filling'], url=item['url'])
            print(hui.filling)
            bot.send_message("-1001303379218", hui.header + hui.filling + hui.url, parse_mode='markdown')
            hui.save()


def main():
    #  x =get_text_binance_article("https://support.binance.com/hc/en-us/articles/360004692771-Binance-Supports-ONT-Mainnet-Swap-and-Adds-ONT-USDT-Trading-Pair-")
    #  Post(header = 	x["header"], filling = x["filling"], url=x["url"]).save()
    #  print(get_text_binance_article("https://support.binance.com/hc/en-us/articles/360004692771-Binance-Supports-ONT-Mainnet-Swap-and-Adds-ONT-USDT-Trading-Pair-")['filling'])
    bot.send_message(chat_id = CHAT,
                     text = (get_first_5news_binance()[0]['filling']),
                     parse_mode = 'markdown'
                     )
    check_save_send_binance(get_first_5news_binance())
    bot.send_message(chat_id=CHAT,text='zaebalo', parse_mode='markdown')
    #  print(get_first_5news())


if __name__ == '__main__':
    main()



