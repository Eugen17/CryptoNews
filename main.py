from binance import check_save_send_binance, get_first_news_binance
from bitrumb import check_save_send_bitrumb, get_first_news_bitrumb
from okex import check_save_send_okex, get_first_news_okex
from upbit import check_save_send_upbit, get_first_news_upbit
from binance_news2 import check_save_send_binance2, get_first_references_binance2, get_first_news_binance2
from logger_settings import logger
import time


# У тебя все равно слипы по 3 сек - запусти все в одном потоке поочереди и слип между каждым сделай 1 с
# На исключении вызывай логгер from logger_settings import logger | при исключении - logger.exception('[E]')
# Не зназывай файл "меин" - назови ран_проджект
# Поменяй все тебы на 4 пробела
# Остальной кодстайл тоже поправь
# Выпили все что не юзаешь
# Выпили принты - юзай логгер
# Слип вне трая должен быть как по мне. Он то не вылетит
# def bitrumb_post():
#     while True:
#         try:
#             time.sleep(3)
#             check_save_send_bitrumb(get_first_5news_bitrumb())
#             print("rabotaem1")
#         except:
#             pass
#
#
# def okex_post():
#     while True:
#         try:
#             time.sleep(3)
#             check_save_send_okex(get_first_news_okex())
#             print("rabotaem2")
#         except:
#             pass
#
#
# def binance_post():
#     while True:
#         try:
#             check_save_send_binance(get_first_5news_binance())
#             print("rabotaem3")
#         except:
#             pass


def main():
    # Thread(target=bitrumb_post).start()
    # Thread(target=okex_post).start()
    # Thread(target=binance_post).start()



    while True:
        try:
            check_save_send_bitrumb(get_first_news_bitrumb())
            check_save_send_okex(get_first_news_okex())
            check_save_send_binance(get_first_news_binance())
            check_save_send_binance2(get_first_news_binance2())
            
        except Exception:
            logger.exception('[E]')


if __name__ == '__main__':
    main()
