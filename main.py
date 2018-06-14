from binance import check_save_send_binance, get_first_5news_binance
from bitrumb import check_save_send_bitrumb, get_first_5news_bitrumb
from okex import check_save_send_okex, get_first_news_okex
from threading import Thread
import time


def bitrumb_post():
	while (True):
		try:
			time.sleep(3)
			check_save_send_bitrumb(get_first_5news_bitrumb())
			print ("rabotaem1")
		except:
			pass	


def okex_post():
	while (True):
		try:
			time.sleep(3)
			check_save_send_okex(get_first_news_okex())
			print ("rabotaem2")
		except:
			pass	


def binance_post():
	while (True):
		try:
			time.sleep(3)
			check_save_send_binance(get_first_5news_binance())
			print ("rabotaem3")
		except :
			pass
		
		




def main():
	Thread(target=bitrumb_post).start()
	Thread(target=okex_post).start()
	Thread(target=binance_post).start()

if __name__ == '__main__':
	main()