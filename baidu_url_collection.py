#coding=utf-8

import requests
import re
import Queue
import threading
from bs4 import BeautifulSoup as bs
import os,sys,time

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}


class BaiduSpider(threading.Thread):
	def __init__(self,queue):
		threading.Thread.__init__(self)
		self._queue = queue
	def run(self):
		while not self._queue.empty():
			url = self._queue.get_nowait()
			try:
				#print url
				self.spider(url)
			except Exception,e:
				print e
				pass

	def spider(self,url):
	#if not add self , error:takes exactly 1 argument (2 given)	
		r = requests.get(url=url,headers=headers)
		soup = bs(r.content,'lxml')
		urls = soup.find_all(name='a',attrs={'data-click':re.compile(('.')),'class':None})
		for url in urls:
			#print url['href']
			new_r = requests.get(url=url['href'],headers=headers,timeout=3)
			if new_r.status_code == 200 :
				url_para = new_r.url
				url_index_tmp = url_para.split('/')
				url_index = url_index_tmp[0]+'//'+url_index_tmp[2]
				print url_para+'\n'+url_index
				with open('url_para.txt','a+') as f1:
					f1.write(url_para+'\n')
				with open('url_index.txt','a+') as f2:
					with open('url_index.txt', 'r') as f3:
						if url_index not in f3.read():
							f2.write(url_index+'\n')
			else:
				print 'no access',url['href']

def main(keyword):
	queue = Queue.Queue()
	de_keyword = keyword.decode(sys.stdin.encoding).encode('utf-8')
	print keyword
	# baidu max pages 76 , so pn=750 max
	for i in range(0,760,10):
		#queue.put('https://www.baidu.com/s?ie=utf-8&wd=%s&pn=%d'%(keyword,i))
		queue.put('https://www.baidu.com/s?ie=utf-8&wd=%s&pn=%d'%(de_keyword,i))
	threads = []
	thread_count = 4
	for i in range(thread_count):
		threads.append(BaiduSpider(queue))
	for t in threads:
		t.start()
	for t in threads:
		t.join()

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Enter:%s keyword'%sys.argv[0]
		sys.exit(-1)
	else:
		main(sys.argv[1])	
